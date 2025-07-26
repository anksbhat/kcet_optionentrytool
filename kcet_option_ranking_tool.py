import pandas as pd
import re
import os

OPTION_CSV = "data/option_entries.csv"
CUTOFF_CSV = "data/cutoff_data_structured.csv"
OUTPUT_CSV = "data/option_entries_ranked.csv"

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

def prompt_priority(options, col_name, prompt):
    unique_items = options[col_name].unique().tolist()
    print(f"\n{prompt}")
    for idx, item in enumerate(unique_items):
        print(f"{idx+1}. {item}")
    print("Enter your priorities as comma-separated numbers (e.g. 2,1,3,...), or press Enter to skip:")
    sel = input().strip()
    if sel:
        order = [unique_items[int(i)-1] for i in sel.split(",") if i.isdigit() and 1 <= int(i) <= len(unique_items)]
        priority_map = {item: idx for idx, item in enumerate(order)}
        return options[col_name].map(lambda x: priority_map.get(x, len(order)))
    else:
        return [0]*len(options)

def match_and_rank_options(option_csv, cutoff_csv, output_csv, category):
    options = pd.read_csv(option_csv)
    cutoff = pd.read_csv(cutoff_csv)
    ranks = []
    for _, opt in options.iterrows():
        college_id = re.match(r"(E\d{3,4})", opt["College_Code"]).group(1)
        course_name = opt["Course_Name"].replace("&", "AND").upper().replace("  ", " ").strip()
        match = cutoff[(cutoff["College_ID"] == college_id) & (cutoff["Course_Name"].str.upper().str.replace("  ", " ").str.contains(course_name[:10]))]
        if not match.empty:
            rank = match.iloc[0][category]
        else:
            rank = "NOT FOUND"
        ranks.append(rank)
    options["rank"] = ranks
    options["rank_numeric"] = pd.to_numeric(options["rank"], errors="coerce")
    # Prompt for college priority
    options["college_priority"] = prompt_priority(options, "College_Name_Clean", "Select your college priority (most preferred first):")
    # Prompt for branch priority
    options["branch_priority"] = prompt_priority(options, "Course_Name", "Select your branch/course priority (most preferred first):")
    # Sort by rank, then college, then branch priority
    options_sorted = options.sort_values(by=["rank_numeric", "college_priority", "branch_priority"], ascending=True)
    options_sorted.drop(columns=["rank_numeric", "college_priority", "branch_priority"], inplace=True)
    options_sorted.to_csv(output_csv, index=False)
    print(f"✅ Final ranked options saved to {output_csv}")
    print(options_sorted.head())

def main():
    print("KCET Option Entry Ranking Tool - Unified Workflow")
    # Assume CSVs are already parsed and available
    category = get_user_category()
    match_and_rank_options(OPTION_CSV, CUTOFF_CSV, OUTPUT_CSV, category)

if __name__ == "__main__":
    main()
