import pandas as pd
import glob

files = glob.glob("table6_2026_*.csv")
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
df.to_csv("table6_all_months.csv", index=False)
print(f"Total combined rows: {len(df)}")
print(f"Unique projects: {df['project_code'].nunique()}")