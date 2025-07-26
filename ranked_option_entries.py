import pandas as pd

INPUT_CSV = "data/option_entries_with_rank.csv"
OUTPUT_CSV = "data/option_entries_ranked.csv"

def main():
    df = pd.read_csv(INPUT_CSV)
    # Convert rank to numeric, set errors='coerce' to handle 'NOT FOUND'
    df['rank_numeric'] = pd.to_numeric(df['rank'], errors='coerce')
    df_sorted = df.sort_values(by='rank_numeric', ascending=True)
    df_sorted.drop(columns=['rank_numeric'], inplace=True)
    df_sorted.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Ranked options saved to {OUTPUT_CSV}")
    print(df_sorted.head())

if __name__ == "__main__":
    main()
