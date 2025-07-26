import pdfplumber
import pandas as pd
import re

PDF_PATH = "2025cutofflistmock.pdf"
CSV_PATH = "data/cutoff_data_structured.csv"

# Define the 24 KCET categories (update as needed)
CATEGORY_COLS = [
    "1G", "1K", "1R", "2AG", "2AK", "2AR", "2BG", "2BK", "2BR", "3AG", "3AK", "3AR", "3BG", "3BK", "3BR", "GM", "GMK", "GMR", "SCG", "SCK", "SCR", "STG", "STK", "STR"
]

COLUMNS = ["College_ID", "College_Name", "Course_Name"] + CATEGORY_COLS

def parse_cutoff_pdf(pdf_path):
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")
            college_id = None
            college_name = None
            # Scan lines for college header
            for idx, line in enumerate(lines):
                match = re.match(r"(E\d{3,4})\s*-\s*(.+)", line)
                if match:
                    college_id = match.group(1).strip()
                    college_name = match.group(2).strip()
            # Extract tables and associate with current college
            tables = page.extract_tables()
            if college_id and college_name:
                for table in tables:
                    for row in table:
                        if row and len(row) >= 25:
                            course_name = row[0].strip()
                            cutoff_ranks = [r.strip() for r in row[1:25]]
                            rows.append([college_id, college_name, course_name] + cutoff_ranks)
    return pd.DataFrame(rows, columns=COLUMNS)

def main():
    df = parse_cutoff_pdf(PDF_PATH)
    df.to_csv(CSV_PATH, index=False)
    print(f"✅ Parsed cutoff data and saved to {CSV_PATH}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Rows: {len(df)}")

if __name__ == "__main__":
    main()
