import pandas as pd

xl = pd.ExcelFile('Travler Week 4 Paid Advertising Dataset.xlsx')
print("SHEETS:", xl.sheet_names)
print()
for sheet in xl.sheet_names:
    df = xl.parse(sheet)
    print(f"=== {sheet} ===")
    print(df.to_string())
    print()
