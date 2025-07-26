import pdfplumber
import pandas as pd
import re

PDF_PATH = "2025cutofflistmock.pdf"
CSV_PATH = "data/cutoff_data_structured.csv"

CATEGORY_COLS = [
    "1G", "1K", "1R", "2AG", "2AK", "2AR", "2BG", "2BK", "2BR", "3AG", "3AK", "3AR", "3BG", "3BK", "3BR", "GM", "GMK", "GMR", "SCG", "SCK", "SCR", "STG", "STK", "STR"
]
COLUMNS = ["College_ID", "College_Name", "Course_Name"] + CATEGORY_COLS

def extract_all_pages(pdf_path):
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            college_headers = re.findall(r"College: \((E\d{3,4})\)([^\n]+)", text)
            tables = page.extract_tables()
            for idx, table in enumerate(tables):
                if idx < len(college_headers):
                    college_id, college_name = college_headers[idx]
                    for row in table[1:]:  # skip header row
                        if row and len(row) >= 25:
                            course_name = row[0].replace("\n", " ").strip()
                            cutoff_ranks = [r.strip() for r in row[1:25]]
                            rows.append([college_id.strip(), college_name.strip(), course_name] + cutoff_ranks)
    return pd.DataFrame(rows, columns=COLUMNS)

def main():
    df = extract_all_pages(PDF_PATH)
    df.to_csv(CSV_PATH, index=False)
    print(f"✅ Extracted first page cutoff data and saved to {CSV_PATH}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Rows: {len(df)}")
    print(df.head())

if __name__ == "__main__":
    main()
