import streamlit as st
import pandas as pd
import re
import os
from io import BytesIO

st.set_page_config(page_title="KCET Option Ranking Tool", layout="wide")
st.title("KCET Option Ranking Tool")

CATEGORY_COLS = [
    "1G", "1K", "1R", "2AG", "2AK", "2AR", "2BG", "2BK", "2BR", "3AG", "3AK", "3AR", "3BG", "3BK", "3BR", "GM", "GMK", "GMR", "SCG", "SCK", "SCR", "STG", "STK", "STR"
]

CUTOFF_CSV = "data/cutoff_data_structured.csv"


# Step 1: Upload option entry PDF
pdf_file = st.file_uploader("Upload your Option Entry PDF", type=["pdf"])

def parse_option_entry_pdf(pdf_bytes):
    import pdfplumber
    import io
    pdf = pdfplumber.open(io.BytesIO(pdf_bytes))
    entries = []
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split("\n")
        for line in lines:
            # Improved pattern: Option_No, College_Code, Course_Name, Course_Fee, College_Name
            match = re.match(r"(\d+)\s+(E\d{3,4}[A-Z]*)\s+(.+?)\s+([\d,\- ]+.*?Lakh.*?Thousand.*?)\s+(.+)", line)
            if match:
                fee = match.group(4)
                college_name_raw = match.group(5)
                # Remove any trailing fee text from college name if present
                college_name = re.sub(r"Lakh.*?Thousand.*", "", college_name_raw).strip()
                entries.append({
                    "Option_No": match.group(1),
                    "College_Code": match.group(2),
                    "Course_Name": match.group(3),
                    "Course_Fee": fee,
                    "College_Name": college_name,
                    "College_Name_Clean": college_name.split(',')[0].strip()
                })
    pdf.close()
    return pd.DataFrame(entries)

if pdf_file:
    options = parse_option_entry_pdf(pdf_file.read())
    if options.empty:
        st.error("Could not parse any option entries from the PDF. Please check the format.")
    else:
        st.success(f"Parsed {len(options)} option entries from PDF.")
        # Step 2: Select KCET category
        category = st.selectbox("Select your KCET category", CATEGORY_COLS, index=15)
        # Step 3: Set college priority
        colleges = options["College_Name_Clean"].unique().tolist()
        college_priority = st.multiselect("Select and order your college priority (most preferred first)", colleges, default=colleges)
        # Step 4: Set branch priority
        branches = options["Course_Name"].unique().tolist()
        branch_priority = st.multiselect("Select and order your branch/course priority (most preferred first)", branches, default=branches)
        # Step 5: Load cutoff data
        cutoff = pd.read_csv(CUTOFF_CSV)
        # Step 6: Match ranks
        ranks = []
        for _, opt in options.iterrows():
            college_id = re.match(r"(E\d{3,4})", str(opt["College_Code"]))
            college_id = college_id.group(1) if college_id else ""
            course_name = str(opt["Course_Name"]).replace("&", "AND").upper().replace("  ", " ").strip()
            match = cutoff[(cutoff["College_ID"] == college_id) & (cutoff["Course_Name"].str.upper().str.replace("  ", " ").str.contains(course_name[:10]))]
            if not match.empty:
                rank = match.iloc[0][category]
            else:
                rank = "NOT FOUND"
            ranks.append(rank)
        options["rank"] = ranks
        options["rank_numeric"] = pd.to_numeric(options["rank"], errors="coerce")
        # Step 7: Apply priorities
        priority_map = {name: idx for idx, name in enumerate(college_priority)}
        options["college_priority"] = options["College_Name_Clean"].map(lambda x: priority_map.get(x, len(priority_map)))
        branch_map = {name: idx for idx, name in enumerate(branch_priority)}
        options["branch_priority"] = options["Course_Name"].map(lambda x: branch_map.get(x, len(branch_map)))
        # Step 8: Sort
        options_sorted = options.sort_values(by=["rank_numeric", "college_priority", "branch_priority"], ascending=True)
        options_sorted.drop(columns=["rank_numeric", "college_priority", "branch_priority"], inplace=True)
        st.subheader("Your Ranked KCET Options List")
        # Build a styled HTML list
        html = "<div style='font-family:Arial;'>"
        for i, row in enumerate(options_sorted.itertuples(index=False), 1):
            html += f"<div style='background:#f8f9fa;border-radius:8px;padding:10px;margin-bottom:8px;box-shadow:0 1px 3px #ccc;'>"
            html += f"<span style='font-size:18px;font-weight:bold;color:#0072C6;'>{i}. {row.College_Name_Clean}</span>"
            html += f"<br><span style='font-size:16px;color:#333;'>{row.Course_Name}</span>"
            html += f"<br><span style='font-size:15px;color:#666;'>Rank: <b>{row.rank}</b></span>"
            html += "</div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
        # Step 9: Download CSV
        csv_bytes = BytesIO()
        options_sorted.to_csv(csv_bytes, index=False)
        st.download_button("Download Ranked CSV", data=csv_bytes.getvalue(), file_name="KCET_Option_Entry_Ranked.csv", mime="text/csv")
        # Step 10: Download PDF
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
else:
    st.info("Please upload your option entry PDF to begin.")
