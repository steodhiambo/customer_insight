import pandas as pd

def explore_excel(file_path):
    xl = pd.ExcelFile(file_path)
    print(f"Sheet names: {xl.sheet_names}")
    for sheet in xl.sheet_names:
        print(f"\n--- Sheet: {sheet} ---")
        df = pd.read_excel(file_path, sheet_name=sheet)
        print(df.head())
        print(df.info())

if __name__ == "__main__":
    explore_excel('Travler Week 5 Funnel and Conversion Dataset.xlsx')
