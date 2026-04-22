import pandas as pd

xl = pd.ExcelFile('Travler Week 3 Campaign and Sentiment Dataset.xlsx')
camp = xl.parse('Campaign Performance', header=2)
camp.columns = ['Campaign_ID','Platform','Audience','Impressions','Clicks','CTR','Cost_KES','Bookings','Conv_Rate']
camp = camp.dropna(subset=['Campaign_ID'])
camp['Cost_KES'] = pd.to_numeric(camp['Cost_KES'])
camp['Bookings'] = pd.to_numeric(camp['Bookings'])
camp['Conv_Rate'] = pd.to_numeric(camp['Conv_Rate'])
camp['CPA'] = camp['Cost_KES'] / camp['Bookings']

print(camp[['Campaign_ID','Platform','Audience','Cost_KES','Bookings','Conv_Rate','CPA']].to_string(index=False))
print()
print(f"Best  Conv Rate: {camp.loc[camp['Conv_Rate'].idxmax(), 'Campaign_ID']} — {camp['Conv_Rate'].max():.1f}%  |  CPA: KES {camp.loc[camp['Conv_Rate'].idxmax(), 'CPA']:.0f}")
print(f"Worst Conv Rate: {camp.loc[camp['Conv_Rate'].idxmin(), 'Campaign_ID']} — {camp['Conv_Rate'].min():.1f}%  |  CPA: KES {camp.loc[camp['Conv_Rate'].idxmin(), 'CPA']:.0f}")
print(f"Best  CPA:       {camp.loc[camp['CPA'].idxmin(), 'Campaign_ID']} — KES {camp['CPA'].min():.0f}  |  Conv Rate: {camp.loc[camp['CPA'].idxmin(), 'Conv_Rate']:.1f}%")
print(f"Worst CPA:       {camp.loc[camp['CPA'].idxmax(), 'Campaign_ID']} — KES {camp['CPA'].max():.0f}  |  Conv Rate: {camp.loc[camp['CPA'].idxmax(), 'Conv_Rate']:.1f}%")
