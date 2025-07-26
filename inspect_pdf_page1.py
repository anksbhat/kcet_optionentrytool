import pdfplumber

PDF_PATH = "2025cutofflistmock.pdf"

with pdfplumber.open(PDF_PATH) as pdf:
    page = pdf.pages[0]
    text = page.extract_text()
    print("--- Extracted Text ---")
    print(text)
    print("\n--- Extracted Tables ---")
    tables = page.extract_tables()
    for idx, table in enumerate(tables):
        print(f"\nTable {idx+1}:")
        for row in table:
            print(row)
