import streamlit as st
import pandas as pd
import re
import os
from io import BytesIO
from rapidfuzz import fuzz, process

st.set_page_config(page_title="KCET option entry helper tool", layout="wide")
st.title("KCET option entry helper tool")

CATEGORY_COLS = [
    "1G", "1K", "1R", "2AG", "2AK", "2AR", "2BG", "2BK", "2BR", "3AG", "3AK", "3AR", "3BG", "3BK", "3BR", "GM", "GMK", "GMR", "SCG", "SCK", "SCR", "STG", "STK", "STR"
]

CUTOFF_CSV = "data/cutoff_data_structured.csv"



# Step 1: Upload option entry PDF
pdf_file = st.file_uploader("Upload your Option Entry PDF", type=["pdf"])




def parse_option_entry_pdf_standard(pdf_bytes):
    import pdfplumber
    import io
    pdf = pdfplumber.open(io.BytesIO(pdf_bytes))
    entries = []
    fee_pattern = re.compile(r"[\d,]+\s*-\s*One Lakh.*?Thousand.*", re.IGNORECASE)
    for page in pdf.pages:
        # Try to extract tables from the page
        tables = page.extract_tables()
        for table in tables:
            # Skip empty or malformed tables
            if not table or len(table) < 2:
                continue
            # Try to find header row (assume first row is header if it contains 'option' or 'college')
            header_row = table[0]
            # Heuristic: Find columns by keywords
            col_map = {}
            for idx, col in enumerate(header_row):
                if col:
                    col_l = col.lower()
                    if 'option' in col_l:
                        col_map['Option_No'] = idx
                    elif 'college code' in col_l or 'code' in col_l:
                        col_map['College_Code'] = idx
                    elif 'course' in col_l or 'branch' in col_l:
                        col_map['Course_Name'] = idx
                    elif 'fee' in col_l:
                        col_map['Course_Fee'] = idx
                    elif 'college name' in col_l or 'institute' in col_l:
                        col_map['College_Name'] = idx
            # If not all columns found, use default positions (KCET PDFs are usually fixed format)
            if not col_map or len(col_map) < 4:
                # Assume: 0=Option_No, 1=College_Code, 2=Course_Name, 3=Course_Fee, 4=College_Name
                col_map = {'Option_No': 0, 'College_Code': 1, 'Course_Name': 2, 'Course_Fee': 3, 'College_Name': 4}
            # Parse each row (skip header)
            for row in table[1:]:
                if not row or len(row) < 3:
                    continue
                option_no = row[col_map.get('Option_No', 0)] if len(row) > col_map.get('Option_No', 0) else ''
                college_code = row[col_map.get('College_Code', 1)] if len(row) > col_map.get('College_Code', 1) else ''
                course_name = row[col_map.get('Course_Name', 2)] if len(row) > col_map.get('Course_Name', 2) else ''
                fee = row[col_map.get('Course_Fee', 3)] if len(row) > col_map.get('Course_Fee', 3) else ''
                college_name = row[col_map.get('College_Name', 4)] if len(row) > col_map.get('College_Name', 4) else ''
                # Clean up
                course_name = str(course_name).replace("  ", " ").strip()
                course_name = re.sub(r"( ENGINEERING)+$", " ENGINEERING", course_name)
                college_name_clean = str(college_name).split(',')[0].strip() if college_name else ""
                entries.append({
                    "Option_No": str(option_no).strip(),
                    "College_Code": str(college_code).strip(),
                    "Course_Name": course_name,
                    "Course_Fee": str(fee).strip(),
                    "College_Name": str(college_name).strip(),
                    "College_Name_Clean": college_name_clean
                })
    pdf.close()
    return pd.DataFrame(entries)

# Placeholder for AI-based extraction using HuggingFace Donut or LayoutLM



if pdf_file:
    options = parse_option_entry_pdf_standard(pdf_file.read())
    if options.empty:
        st.error("Could not parse any option entries from the PDF. Please check the format.")
    else:
        # Remove empty rows (if any) for accurate count
        options_display = options.dropna(how='all')
        st.success(f"Parsed {len(options_display)} option entries from PDF.")
        st.markdown("<h4>Parsed Option Entries (from your PDF):</h4>")
        st.dataframe(options_display, use_container_width=True, height=350)
        # Step 2: Select KCET category
        category = st.selectbox("Select your KCET category", CATEGORY_COLS, index=15)
        # Step 3: Match ranks from cutoff CSV robustly and display all options with their ranks
        cutoff_df = pd.read_csv(CUTOFF_CSV)
        # Use raw College_Name and Course_Name columns for matching
        from rapidfuzz import fuzz, process
        def normalize(s):
            # Remove all non-alphanumeric characters for robust matching
            s = str(s).strip().lower()
            s = re.sub(r"[^a-z0-9]", "", s)
            return s

        ranks = []
        for _, opt in options.iterrows():
            # 1. Exact match
            match = cutoff_df[
                (cutoff_df["College_Name"] == opt["College_Name"]) &
                (cutoff_df["Course_Name"] == opt["Course_Name"])
            ]
            # 2. Case/whitespace-insensitive match
            if match.empty:
                match = cutoff_df[
                    (cutoff_df["College_Name"].apply(normalize) == normalize(opt["College_Name"])) &
                    (cutoff_df["Course_Name"].apply(normalize) == normalize(opt["Course_Name"]))
                ]
            # 3. Substring match
            if match.empty:
                cname_pat = re.escape(opt["College_Name"].strip().lower())
                course_pat = re.escape(opt["Course_Name"].strip().lower())
                match = cutoff_df[
                    (cutoff_df["College_Name"].str.lower().str.contains(cname_pat, na=False, regex=True)) &
                    (cutoff_df["Course_Name"].str.lower().str.contains(course_pat, na=False, regex=True))
                ]
            # 4. Fuzzy match (if still not found)
            if match.empty:
                # Find best fuzzy match for college and course
                best_college = process.extractOne(opt["College_Name"], cutoff_df["College_Name"], scorer=fuzz.token_sort_ratio)
                best_course = process.extractOne(opt["Course_Name"], cutoff_df["Course_Name"], scorer=fuzz.token_sort_ratio)
                if best_college and best_course and best_college[1] > 85 and best_course[1] > 85:
                    match = cutoff_df[
                        (cutoff_df["College_Name"] == best_college[0]) &
                        (cutoff_df["Course_Name"] == best_course[0])
                    ]
            if not match.empty and category in match.columns:
                rank_val = match.iloc[0][category]
            else:
                rank_val = None
            ranks.append(rank_val)
        options["rank"] = ranks
        st.markdown(f"<h5>All Option Entries with Extracted Ranks for <span style='color:#1976d2'>GM</span>:</h5>", unsafe_allow_html=True)
        st.dataframe(options, use_container_width=True, height=500)
        st.info("If a rank is N/A, it means no matching entry was found in the cutoff list for GM category. This could be due to differences in naming, missing data, or unmatched college/course codes. All columns from your parsed option entry are shown below, including the matched rank.")
        # Step 4: Set college priority (ordered)
        college_priority = st.multiselect(
            "Select and order your college priority (most preferred first)",
            options["College_Name"].unique(),
            default=[],
            key="college_priority",
            help="Drag to reorder after selecting."
        )
        # Step 5: Set branch priority (ordered)
        branch_keywords = [
            "computer science", "information science", "biotechnology", "medical electronics", "electronics and communication", "electrical and electronics", "artificial intelligence", "data science", "cyber security", "internet of things", "instrumentation", "mechanical", "civil", "robotics", "chemical", "machine learning", "business", "design"
        ]
        selected_keywords = st.multiselect(
            "Select and order your branch/course priorities (most preferred first)",
            branch_keywords,
            default=[],
            key="branch_priority",
            help="Drag to reorder after selecting."
        )
        # Example line removed as requested
        refresh = st.button("Refresh List")
        # Assign college and branch priority
        def get_college_priority(x):
            try:
                return college_priority.index(x)
            except ValueError:
                return len(college_priority)
        # Improved: For each selected keyword, all course names containing that keyword are grouped by the keyword's order
        def get_branch_priority(x):
            # Only used for sorting, not for extraction or display
            x_lower = x.lower()
            for idx, keyword in enumerate(selected_keywords):
                if keyword.lower() in x_lower:
                    return idx
            return len(selected_keywords)
        options["college_priority_group"] = options["College_Name"].map(get_college_priority)
        options["branch_priority_group"] = options["Course_Name"].map(get_branch_priority)
        # Mutually inclusive ordering: for each branch in branch priority, show all colleges in college priority for that branch, then fallback to remaining options
        if refresh or (not selected_keywords and not college_priority):
            filtered = []
            used_idx = set()
            def rank_sort(df):
                return df.assign(_rank_num=pd.to_numeric(df['rank'], errors='coerce')).sort_values('_rank_num')
            # 1. For each branch in branch priority, for each college in college priority, add matching options
            for branch in selected_keywords:
                for college in college_priority:
                    mask = (
                        options["College_Name"] == college
                    ) & (
                        options["Course_Name"].str.lower().str.contains(branch.lower())
                    )
                    for idx, row in rank_sort(options[mask]).iterrows():
                        if idx not in used_idx:
                            filtered.append(row)
                            used_idx.add(idx)
            # 2. Add remaining options for selected colleges (other branches)
            for college in college_priority:
                mask = (options["College_Name"] == college) & (~options.index.isin(used_idx))
                for idx, row in rank_sort(options[mask]).iterrows():
                    filtered.append(row)
                    used_idx.add(idx)
            # 3. Add remaining options for selected branches (other colleges)
            for branch in selected_keywords:
                mask = (options["Course_Name"].str.lower().str.contains(branch.lower())) & (~options.index.isin(used_idx))
                for idx, row in rank_sort(options[mask]).iterrows():
                    filtered.append(row)
                    used_idx.add(idx)
            # 4. Add all other options (not in any priority)
            for idx, row in rank_sort(options[~options.index.isin(used_idx)]).iterrows():
                filtered.append(row)
                used_idx.add(idx)
            options_sorted = pd.DataFrame(filtered)
            # Minimalistic list UI
            st.markdown("<h3 style='text-align:center; margin-bottom: 0.5em;'>Your Ranked KCET Options List</h3>", unsafe_allow_html=True)
            st.markdown("""
            <div style='width:100%;'>
            <ol style='padding-left: 1.2em; margin-top: 0;'>
            """ +
            "\n".join([
                f"<li style='margin-bottom:6px; font-size:1.05em;'><b>{row['College_Name']}</b> - <span style='font-weight:500;'>{row['Course_Name']}</span> <span style='color:#888; font-size:0.95em;'>Rank: {row['rank'] if pd.notnull(row['rank']) else 'N/A'}</span></li>"
                for _, row in options_sorted.iterrows()
            ]) +
            """
            </ol>
            </div>
            """, unsafe_allow_html=True)
            # Download CSV
            csv_bytes = BytesIO()
            options_sorted.to_csv(csv_bytes, index=False)
            st.download_button("Download Ranked CSV", data=csv_bytes.getvalue(), file_name="KCET_Option_Entry_Ranked.csv", mime="text/csv")
            # Download PDF
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="KCET Option Entry Ranked List", ln=True, align='C')
            for i, row in enumerate(options_sorted.itertuples(index=False), 1):
                line = f"{i}. {row.College_Name_Clean} - {row.Course_Name} | Rank: {row.rank}"
                pdf.cell(0, 10, txt=line, ln=True)
            pdf_bytes = BytesIO(pdf.output(dest='S').encode('latin-1'))
            st.download_button("Download Ranked List as PDF", data=pdf_bytes.getvalue(), file_name="KCET_Option_Entry_Ranked.pdf", mime="application/pdf")
        # After matching ranks, show the parsed table with the rank column
        st.markdown("<h4>Parsed Option Entries with Ranks:</h4>")
        st.dataframe(options[[col for col in options.columns if col != 'rank'] + ['rank']], use_container_width=True, height=600)
else:
    st.info("Please upload your option entry PDF to begin.")
