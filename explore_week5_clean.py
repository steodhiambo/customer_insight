import pandas as pd

def explore_excel_clean(file_path):
    xl = pd.ExcelFile(file_path)
    print(f"Sheet names: {xl.sheet_names}")
    
    # Booking Funnel
    df_funnel = pd.read_excel(file_path, sheet_name='Booking Funnel', skiprows=2)
    print("\n--- Sheet: Booking Funnel ---")
    print(df_funnel)
    
    # User Behaviour
    df_behaviour = pd.read_excel(file_path, sheet_name='User Behaviour', skiprows=2)
    print("\n--- Sheet: User Behaviour ---")
    print(df_behaviour)
    
    # Drop-off Reasons
    df_reasons = pd.read_excel(file_path, sheet_name='Drop-off Reasons', skiprows=2)
    print("\n--- Sheet: Drop-off Reasons ---")
    print(df_reasons)

if __name__ == "__main__":
    explore_excel_clean('Travler Week 5 Funnel and Conversion Dataset.xlsx')
