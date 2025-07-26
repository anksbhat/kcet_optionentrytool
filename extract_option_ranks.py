import pandas as pd
import re

OPTION_CSV = "data/option_entries.csv"
CUTOFF_CSV = "data/cutoff_data_structured.csv"
OUTPUT_CSV = "data/option_entries_with_rank.csv"

CATEGORY_COLS = [
    "1G", "1K", "1R", "2AG", "2AK", "2AR", "2BG", "2BK", "2BR", "3AG", "3AK", "3AR", "3BG", "3BK", "3BR", "GM", "GMK", "GMR", "SCG", "SCK", "SCR", "STG", "STK", "STR"
]

def get_user_category():
    print("Select your KCET category:")
    for idx, cat in enumerate(CATEGORY_COLS):
        print(f"{idx+1}. {cat}")
    sel = input("Enter category number or code: ").strip()
    if sel.isdigit():
        sel = int(sel)
        if 1 <= sel <= len(CATEGORY_COLS):
            return CATEGORY_COLS[sel-1]
    elif sel in CATEGORY_COLS:
        return sel
    print("Invalid selection. Defaulting to GM.")
    return "GM"

def main():
    category = get_user_category()
    print(f"Selected category: {category}")
    options = pd.read_csv(OPTION_CSV)
    cutoff = pd.read_csv(CUTOFF_CSV)
    ranks = []
    for _, opt in options.iterrows():
        college_id = re.match(r"(E\d{3,4})", opt["College_Code"]).group(1)
        course_name = opt["Course_Name"].replace("&", "AND").upper().replace("  ", " ").strip()
        # Try to match course name in cutoff (case-insensitive, ignore extra spaces)
        match = cutoff[(cutoff["College_ID"] == college_id) & (cutoff["Course_Name"].str.upper().str.replace("  ", " ").str.contains(course_name[:10]))]
        if not match.empty:
            rank = match.iloc[0][category]
        else:
            rank = "NOT FOUND"
        ranks.append(rank)
    options["rank"] = ranks
    options.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Output saved to {OUTPUT_CSV}")
    print(options.head())

if __name__ == "__main__":
    main()
