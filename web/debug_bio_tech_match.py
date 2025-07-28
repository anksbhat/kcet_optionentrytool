import pandas as pd
import re

# Load data
options = pd.read_csv(r"c:/Users/z0052dbf/OneDrive - Siemens AG/Documents/Anksbhat_projects/portfolio/KCET_OptionEntry/data/option_entries.csv")
cutoff_df = pd.read_csv(r"c:/Users/z0052dbf/OneDrive - Siemens AG/Documents/Anksbhat_projects/portfolio/KCET_OptionEntry/data/cutoff_data_structured.csv")

def normalize(s):
    s = str(s).strip().lower()
    s = re.sub(r"\s*-\s*", "-", s)
    s = s.replace(" ", "")
    return s

# Find the specific option entry
row = options[(options['College_Name'].str.contains('PES University 100 Feet Ring Road', case=False)) & (options['Course_Name'].str.contains('BIO-TECHNOLOGY', case=False))]
if row.empty:
    print("No matching option entry found.")
    exit()
opt = row.iloc[0]
print("Option Entry:")
print(f"College: {opt['College_Name']}")
print(f"Course: {opt['Course_Name']}")
print(f"Normalized College: {normalize(opt['College_Name'])}")
print(f"Normalized Course: {normalize(opt['Course_Name'])}")

# Show all cutoff candidates for this college
candidates = cutoff_df[cutoff_df['College_Name'].str.contains('PES University 100 Feet Ring Road', case=False)]
print(f"\nCutoff candidates for this college: {len(candidates)}")
for i, cand in candidates.iterrows():
    print(f"\nCutoff College: {cand['College_Name']}")
    print(f"Cutoff Course: {cand['Course_Name']}")
    print(f"Normalized College: {normalize(cand['College_Name'])}")
    print(f"Normalized Course: {normalize(cand['Course_Name'])}")
    print(f"GM Rank: {cand['GM'] if 'GM' in cand else 'N/A'}")
    # Check normalized match
    if normalize(cand['College_Name']) == normalize(opt['College_Name']) and normalize(cand['Course_Name']) == normalize(opt['Course_Name']):
        print("*** NORMALIZED MATCH FOUND ***")
