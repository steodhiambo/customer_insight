import pandas as pd

xl = pd.ExcelFile('Travler Week 3 Campaign and Sentiment Dataset.xlsx')
camp = xl.parse('Campaign Performance', header=2)
camp.columns = ['Campaign_ID','Platform','Audience','Impressions','Clicks','CTR','Cost_KES','Bookings','Conv_Rate']
camp = camp.dropna(subset=['Campaign_ID'])
camp['Cost_KES'] = pd.to_numeric(camp['Cost_KES'])
camp['Bookings'] = pd.to_numeric(camp['Bookings'])
camp['CPA'] = camp['Cost_KES'] / camp['Bookings']

print(camp[['Campaign_ID','Platform','Audience','Cost_KES','Bookings','CPA']].to_string(index=False))
print()

best = camp.loc[camp['CPA'].idxmin()]
worst = camp.loc[camp['CPA'].idxmax()]

print(f"BEST  CPA: {best['Campaign_ID']} | {best['Platform']} | {best['Audience']} | KES {best['Cost_KES']:.0f} / {best['Bookings']:.0f} bookings = KES {best['CPA']:.0f}")
print(f"WORST CPA: {worst['Campaign_ID']} | {worst['Platform']} | {worst['Audience']} | KES {worst['Cost_KES']:.0f} / {worst['Bookings']:.0f} bookings = KES {worst['CPA']:.0f}")
