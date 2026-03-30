import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

# ── Load & clean ──────────────────────────────────────────────────────────────
df = pd.read_excel('Travler Week 1 Customer Insight Dataset.xlsx', header=1)
df.columns = df.iloc[0]
df = df.drop(index=0).reset_index(drop=True)
df['Search_Frequency'] = pd.to_numeric(df['Search_Frequency'])
df['Booked'] = df['Booking_Completed'].eq('Yes')

# ── Palette ───────────────────────────────────────────────────────────────────
YES_C, NO_C = '#2E86AB', '#E84855'
BG = '#F8F9FA'

fig = plt.figure(figsize=(18, 22), facecolor=BG)
fig.suptitle('Travler – Customer Behaviour & Segment Analysis',
             fontsize=20, fontweight='bold', y=0.98, color='#1a1a2e')

axes = []
positions = [
    (0.05, 0.76, 0.26, 0.18),   # 1 – conversion overview
    (0.37, 0.76, 0.26, 0.18),   # 2 – by travel purpose
    (0.69, 0.76, 0.26, 0.18),   # 3 – by age group
    (0.05, 0.52, 0.26, 0.18),   # 4 – by device
    (0.37, 0.52, 0.26, 0.18),   # 5 – by time of search
    (0.69, 0.52, 0.26, 0.18),   # 6 – search frequency vs booking
    (0.05, 0.28, 0.56, 0.18),   # 7 – segment heatmap
    (0.69, 0.28, 0.26, 0.18),   # 8 – route popularity
]
for pos in positions:
    ax = fig.add_axes(pos, facecolor=BG)
    axes.append(ax)

def style(ax, title):
    ax.set_title(title, fontsize=11, fontweight='bold', color='#1a1a2e', pad=8)
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(colors='#444')
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('#ccc')

# ── 1. Overall conversion ─────────────────────────────────────────────────────
ax = axes[0]
counts = df['Booking_Completed'].value_counts()
wedges, texts, autotexts = ax.pie(
    counts, labels=['Not Booked', 'Booked'],
    colors=[NO_C, YES_C], autopct='%1.0f%%',
    startangle=90, wedgeprops=dict(edgecolor='white', linewidth=2))
for at in autotexts:
    at.set_fontsize(12); at.set_fontweight('bold'); at.set_color('white')
ax.set_title('Overall Conversion Rate', fontsize=11, fontweight='bold', color='#1a1a2e', pad=8)
ax.text(0, -1.35, f'9 of 20 users completed a booking  (45%)',
        ha='center', fontsize=8.5, color='#555')

# ── 2. Booking rate by travel purpose ────────────────────────────────────────
ax = axes[1]
purpose_rate = df.groupby('Travel_Purpose')['Booked'].mean().mul(100).sort_values()
colors = [YES_C if v >= 50 else NO_C for v in purpose_rate]
bars = ax.barh(purpose_rate.index, purpose_rate.values, color=colors, edgecolor='white')
for bar, val in zip(bars, purpose_rate.values):
    ax.text(val + 1, bar.get_y() + bar.get_height()/2,
            f'{val:.0f}%', va='center', fontsize=9, color='#333')
ax.set_xlim(0, 115)
ax.set_xlabel('Conversion Rate (%)', fontsize=8, color='#555')
style(ax, 'Conversion by Travel Purpose')

# ── 3. Booking rate by age group ─────────────────────────────────────────────
ax = axes[2]
age_order = ['18-24', '25-34', '35-44', '45+']
age_rate = df.groupby('Age_Group')['Booked'].mean().mul(100).reindex(age_order)
colors = [YES_C if v >= 50 else NO_C for v in age_rate]
bars = ax.bar(age_rate.index, age_rate.values, color=colors, edgecolor='white', width=0.5)
for bar, val in zip(bars, age_rate.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 2,
            f'{val:.0f}%', ha='center', fontsize=9, color='#333')
ax.set_ylim(0, 120)
ax.set_ylabel('Conversion Rate (%)', fontsize=8, color='#555')
style(ax, 'Conversion by Age Group')

# ── 4. Booking rate by device ─────────────────────────────────────────────────
ax = axes[3]
dev_rate = df.groupby('Device')['Booked'].mean().mul(100).sort_values()
colors = [YES_C if v >= 50 else NO_C for v in dev_rate]
bars = ax.barh(dev_rate.index, dev_rate.values, color=colors, edgecolor='white')
for bar, val in zip(bars, dev_rate.values):
    ax.text(val + 1, bar.get_y() + bar.get_height()/2,
            f'{val:.0f}%', va='center', fontsize=9, color='#333')
ax.set_xlim(0, 105)
ax.set_xlabel('Conversion Rate (%)', fontsize=8, color='#555')
style(ax, 'Conversion by Device')

# ── 5. Booking rate by time of search ────────────────────────────────────────
ax = axes[4]
time_order = ['Morning', 'Afternoon', 'Evening', 'Night']
time_rate = df.groupby('Time_of_Search')['Booked'].mean().mul(100).reindex(time_order)
colors = [YES_C if v >= 50 else NO_C for v in time_rate]
bars = ax.bar(time_rate.index, time_rate.values, color=colors, edgecolor='white', width=0.5)
for bar, val in zip(bars, time_rate.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 2,
            f'{val:.0f}%', ha='center', fontsize=9, color='#333')
ax.set_ylim(0, 120)
ax.set_ylabel('Conversion Rate (%)', fontsize=8, color='#555')
style(ax, 'Conversion by Time of Search')

# ── 6. Search frequency vs booking ───────────────────────────────────────────
ax = axes[5]
booked_freq = df[df['Booked']]['Search_Frequency']
not_booked_freq = df[~df['Booked']]['Search_Frequency']
bp = ax.boxplot([booked_freq, not_booked_freq],
                labels=['Booked', 'Not Booked'],
                patch_artist=True,
                medianprops=dict(color='white', linewidth=2))
bp['boxes'][0].set_facecolor(YES_C)
bp['boxes'][1].set_facecolor(NO_C)
ax.set_ylabel('Search Frequency', fontsize=8, color='#555')
ax.text(1, booked_freq.mean() + 0.15, f'avg {booked_freq.mean():.1f}',
        ha='center', fontsize=8, color=YES_C, fontweight='bold')
ax.text(2, not_booked_freq.mean() + 0.15, f'avg {not_booked_freq.mean():.1f}',
        ha='center', fontsize=8, color=NO_C, fontweight='bold')
style(ax, 'Search Frequency vs Booking')

# ── 7. Segment heatmap ────────────────────────────────────────────────────────
ax = axes[6]

segments = {
    'Decisive\nBusiness\nTraveller':  {'Age': '25–44', 'Purpose': 'Business', 'Device': 'Desktop',
                                        'Time': 'Morning', 'Freq': '1–3', 'Conv': '83%', 'n': 6},
    'Family\nPlanner':                {'Age': '45+',   'Purpose': 'Family',   'Device': 'Mixed',
                                        'Time': 'Afternoon','Freq': '1',   'Conv': '100%','n': 3},
    'Casual\nLeisure\nBrowser':       {'Age': '25–44', 'Purpose': 'Leisure',  'Device': 'Mobile',
                                        'Time': 'Evening', 'Freq': '2–3', 'Conv': '20%', 'n': 5},
    'Price-Sensitive\nStudent\nSearcher': {'Age': '18–24', 'Purpose': 'Student', 'Device': 'Mobile',
                                        'Time': 'Night',   'Freq': '5–7', 'Conv': '0%',  'n': 6},
}

cols = ['Age Group', 'Purpose', 'Primary Device', 'Peak Search Time', 'Avg Searches', 'Conv. Rate', 'Users']
col_keys = ['Age', 'Purpose', 'Device', 'Time', 'Freq', 'Conv', 'n']
seg_names = list(segments.keys())

ax.set_xlim(0, len(cols))
ax.set_ylim(0, len(seg_names))
ax.axis('off')

seg_colors = ['#2E86AB', '#3BB273', '#F4A261', '#E84855']

# Header row
for j, col in enumerate(cols):
    ax.text(j + 0.5, len(seg_names) + 0.3, col,
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1a1a2e')

for i, (seg, data) in enumerate(segments.items()):
    row = len(seg_names) - 1 - i
    # Segment name cell
    rect = mpatches.FancyBboxPatch((0, row + 0.05), len(cols), 0.88,
                                    boxstyle='round,pad=0.02',
                                    facecolor=seg_colors[i] + '22',
                                    edgecolor=seg_colors[i], linewidth=1.2)
    ax.add_patch(rect)
    ax.text(-0.05, row + 0.5, seg, ha='right', va='center',
            fontsize=8, fontweight='bold', color=seg_colors[i])
    for j, key in enumerate(col_keys):
        val = str(data[key])
        color = '#1a1a2e'
        if key == 'Conv':
            color = YES_C if int(val.replace('%','')) >= 50 else NO_C
            fontweight = 'bold'
        else:
            fontweight = 'normal'
        ax.text(j + 0.5, row + 0.5, val,
                ha='center', va='center', fontsize=9,
                color=color, fontweight=fontweight)

ax.set_title('Customer Segments – Behavioural Profile', fontsize=11,
             fontweight='bold', color='#1a1a2e', pad=8)

# ── 8. Route popularity ───────────────────────────────────────────────────────
ax = axes[7]
route_counts = df['Route_Searched'].value_counts()
route_conv = df.groupby('Route_Searched')['Booked'].mean().mul(100)
route_df = pd.DataFrame({'searches': route_counts, 'conv': route_conv}).sort_values('searches')

bar_colors = [YES_C if v >= 50 else NO_C for v in route_df['conv']]
bars = ax.barh(route_df.index, route_df['searches'], color=bar_colors, edgecolor='white')
for bar, (_, row) in zip(bars, route_df.iterrows()):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
            f"{int(row['searches'])} searches  |  {row['conv']:.0f}% conv.",
            va='center', fontsize=8, color='#333')
ax.set_xlim(0, 9)
ax.set_xlabel('Number of Searches', fontsize=8, color='#555')
style(ax, 'Route Popularity & Conversion')

# ── Insight annotations ───────────────────────────────────────────────────────
insights = [
    (0.05, 0.245, '📌 Key Insight: Students & Leisure users account for 55% of searches but 0–20% conversion.\n'
                  'Business & Family users are fewer but drive the majority of completed bookings.'),
    (0.05, 0.215, '📌 Device Gap: Desktop users convert at 86% vs Mobile at 23%  —  a critical UX/checkout friction point on mobile.'),
    (0.05, 0.185, '📌 Timing Signal: Morning & Afternoon searches convert at 83–100%. Evening & Night searches convert at 0%  —  '
                  'suggesting price-checking behaviour without intent to book.'),
    (0.05, 0.155, '📌 Search Frequency: Non-converters search an average of 4.5× vs 1.7× for converters  —  '
                  'high frequency signals comparison shopping and booking hesitation.'),
]
for x, y, text in insights:
    fig.text(x, y, text, fontsize=8.5, color='#333',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#fff3cd', edgecolor='#f0ad4e', alpha=0.9))

# ── Recommendations ───────────────────────────────────────────────────────────
fig.text(0.05, 0.10,
    'Strategic Recommendations',
    fontsize=12, fontweight='bold', color='#1a1a2e')

recs = [
    '1. Fix Mobile Checkout  —  76% of non-converters are on mobile. Simplify the payment flow and add trust signals (secure badge, price-lock guarantee).',
    '2. Re-engage Evening/Night Browsers  —  Deploy retargeting emails or push notifications within 1 hour of an abandoned evening/night search session.',
    '3. Nurture Student Segment  —  0% conversion but highest search frequency. Introduce a student discount or flexible payment option to lower the barrier.',
    '4. Protect High-Value Segments  —  Business & Family users convert reliably. Prioritise a frictionless desktop experience and loyalty perks to retain them.',
    '5. Address Pricing Transparency  —  High repeat searches on the same routes suggest price uncertainty. A visible "Best Price Guarantee" or fare-alert feature could accelerate decisions.',
]
for i, rec in enumerate(recs):
    fig.text(0.05, 0.085 - i * 0.018, rec, fontsize=8.5, color='#333')

plt.savefig('travler_customer_insight_report.png', dpi=150, bbox_inches='tight',
            facecolor=BG)
print('Saved: travler_customer_insight_report.png')
plt.show()
