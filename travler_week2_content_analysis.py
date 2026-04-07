import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

# ── Load & clean ──────────────────────────────────────────────────────────────
xl = pd.ExcelFile('Travler Week 2 Content Dataset.xlsx')

perf = xl.parse('Content Performance', header=2)
perf.columns = ['Post_ID', 'Platform', 'Content_Type', 'Theme',
                'Impressions', 'Likes', 'Comments', 'Shares', 'Clicks', 'Bookings']
for col in ['Impressions', 'Likes', 'Comments', 'Shares', 'Clicks', 'Bookings']:
    perf[col] = pd.to_numeric(perf[col])

aud = xl.parse('Audience Insights', header=2)
aud.columns = ['Segment', 'Age_Group', 'Primary_Device', 'Top_Route',
               'Content_Preference', 'Key_Behaviour']

perf['Engagement_Rate'] = (perf['Likes'] + perf['Comments'] + perf['Shares']) / perf['Impressions'] * 100
perf['Booking_Rate']    = perf['Bookings'] / perf['Impressions'] * 100

# ── Palette ───────────────────────────────────────────────────────────────────
BG       = '#F8F9FA'
C_INST   = '#E1306C'
C_TIKT   = '#010101'
C_X      = '#1DA1F2'
PLATFORM_COLORS = {'Instagram': C_INST, 'TikTok': C_TIKT, 'X': C_X}
THEME_COLOR     = '#2E86AB'
ACCENT          = '#F4A261'

fig = plt.figure(figsize=(18, 22), facecolor=BG)
fig.suptitle('Travler – Week 2 Content Performance & Strategy Report',
             fontsize=20, fontweight='bold', y=0.98, color='#1a1a2e')

positions = [
    (0.05, 0.76, 0.26, 0.18),   # 1 – bookings by theme
    (0.37, 0.76, 0.26, 0.18),   # 2 – impressions vs bookings by platform
    (0.69, 0.76, 0.26, 0.18),   # 3 – engagement rate by format
    (0.05, 0.52, 0.56, 0.18),   # 4 – booking rate per post (scatter)
    (0.69, 0.52, 0.26, 0.18),   # 5 – clicks vs bookings by platform
    (0.05, 0.28, 0.90, 0.18),   # 6 – audience segment table
]
axes = [fig.add_axes(p, facecolor=BG) for p in positions]

def style(ax, title):
    ax.set_title(title, fontsize=11, fontweight='bold', color='#1a1a2e', pad=8)
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(colors='#444')
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('#ccc')

# ── 1. Total bookings by theme ────────────────────────────────────────────────
ax = axes[0]
theme_books = perf.groupby('Theme')['Bookings'].sum().sort_values()
colors = [THEME_COLOR if v >= theme_books.median() else ACCENT for v in theme_books]
bars = ax.barh(theme_books.index, theme_books.values, color=colors, edgecolor='white')
for bar, val in zip(bars, theme_books.values):
    ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
            str(int(val)), va='center', fontsize=9, color='#333')
ax.set_xlabel('Total Bookings', fontsize=8, color='#555')
style(ax, 'Total Bookings by Content Theme')

# ── 2. Impressions vs bookings by platform ────────────────────────────────────
ax = axes[1]
plat = perf.groupby('Platform')[['Impressions', 'Bookings']].sum()
x = range(len(plat))
w = 0.35
bars1 = ax.bar([i - w/2 for i in x], plat['Impressions'] / 1000,
               width=w, label='Impressions (000s)', color='#2E86AB', edgecolor='white')
ax2 = ax.twinx()
bars2 = ax2.bar([i + w/2 for i in x], plat['Bookings'],
                width=w, label='Bookings', color=ACCENT, edgecolor='white')
ax.set_xticks(list(x))
ax.set_xticklabels(plat.index, fontsize=9)
ax.set_ylabel('Impressions (000s)', fontsize=8, color='#2E86AB')
ax2.set_ylabel('Bookings', fontsize=8, color=ACCENT)
ax.spines[['top', 'right']].set_visible(False)
ax2.spines[['top']].set_visible(False)
ax.set_title('Impressions vs Bookings by Platform', fontsize=11,
             fontweight='bold', color='#1a1a2e', pad=8)
handles = [mpatches.Patch(color='#2E86AB', label='Impressions (000s)'),
           mpatches.Patch(color=ACCENT, label='Bookings')]
ax.legend(handles=handles, fontsize=7, loc='upper left')

# ── 3. Avg engagement rate by content format ──────────────────────────────────
ax = axes[2]
fmt_eng = perf.groupby('Content_Type')['Engagement_Rate'].mean().sort_values()
colors = ['#3BB273' if v >= fmt_eng.median() else '#E84855' for v in fmt_eng]
bars = ax.barh(fmt_eng.index, fmt_eng.values, color=colors, edgecolor='white')
for bar, val in zip(bars, fmt_eng.values):
    ax.text(val + 0.05, bar.get_y() + bar.get_height() / 2,
            f'{val:.1f}%', va='center', fontsize=9, color='#333')
ax.set_xlabel('Avg Engagement Rate (%)', fontsize=8, color='#555')
style(ax, 'Avg Engagement Rate by Format')

# ── 4. Booking rate per post (scatter — impressions vs bookings, sized by engagement) ──
ax = axes[3]
platform_list = perf['Platform'].unique()
for plat_name in platform_list:
    sub = perf[perf['Platform'] == plat_name]
    ax.scatter(sub['Impressions'], sub['Bookings'],
               s=sub['Engagement_Rate'] * 40,
               color=PLATFORM_COLORS.get(plat_name, '#999'),
               alpha=0.8, edgecolors='white', linewidth=0.8,
               label=plat_name)
    for _, row in sub.iterrows():
        ax.annotate(row['Post_ID'],
                    (row['Impressions'], row['Bookings']),
                    textcoords='offset points', xytext=(5, 3),
                    fontsize=7, color='#555')
ax.set_xlabel('Impressions', fontsize=8, color='#555')
ax.set_ylabel('Bookings', fontsize=8, color='#555')
ax.legend(fontsize=8, title='Platform', title_fontsize=8)
style(ax, 'Impressions vs Bookings per Post  (bubble size = engagement rate)')

# ── 5. Clicks vs bookings by platform ────────────────────────────────────────
ax = axes[4]
plat_cb = perf.groupby('Platform')[['Clicks', 'Bookings']].sum()
click_to_book = (plat_cb['Bookings'] / plat_cb['Clicks'] * 100).sort_values()
colors = ['#3BB273' if v >= click_to_book.median() else '#E84855' for v in click_to_book]
bars = ax.barh(click_to_book.index, click_to_book.values, color=colors, edgecolor='white')
for bar, val in zip(bars, click_to_book.values):
    ax.text(val + 0.1, bar.get_y() + bar.get_height() / 2,
            f'{val:.1f}%', va='center', fontsize=9, color='#333')
ax.set_xlabel('Click-to-Booking Rate (%)', fontsize=8, color='#555')
style(ax, 'Click-to-Booking Rate by Platform')

# ── 6. Audience segment table ─────────────────────────────────────────────────
ax = axes[5]
ax.axis('off')
seg_colors = ['#2E86AB', '#3BB273', '#F4A261', '#E84855']
cols = ['Segment', 'Age Group', 'Device', 'Top Route', 'Content Preference', 'Key Behaviour']
col_keys = ['Segment', 'Age_Group', 'Primary_Device', 'Top_Route', 'Content_Preference', 'Key_Behaviour']
col_widths = [1.5, 0.8, 0.8, 1.4, 2.2, 2.2]
total_w = sum(col_widths)

ax.set_xlim(0, total_w)
ax.set_ylim(0, len(aud) + 1)

# Header
x_pos = 0
for col, w in zip(cols, col_widths):
    ax.text(x_pos + w / 2, len(aud) + 0.4, col,
            ha='center', va='center', fontsize=9, fontweight='bold', color='#1a1a2e')
    x_pos += w

for i, row in aud.iterrows():
    y = len(aud) - 1 - i
    rect = mpatches.FancyBboxPatch((0, y + 0.05), total_w, 0.88,
                                    boxstyle='round,pad=0.02',
                                    facecolor=seg_colors[i] + '22',
                                    edgecolor=seg_colors[i], linewidth=1.2)
    ax.add_patch(rect)
    x_pos = 0
    for key, w in zip(col_keys, col_widths):
        val = str(row[key])
        fw = 'bold' if key == 'Segment' else 'normal'
        fc = seg_colors[i] if key == 'Segment' else '#1a1a2e'
        ax.text(x_pos + w / 2, y + 0.5, val,
                ha='center', va='center', fontsize=8,
                fontweight=fw, color=fc)
        x_pos += w

ax.set_title('Audience Segments – Content Preferences & Behaviour',
             fontsize=11, fontweight='bold', color='#1a1a2e', pad=8)

# ── Key insights ──────────────────────────────────────────────────────────────
top_theme  = perf.groupby('Theme')['Bookings'].sum().idxmax()
top_format = perf.groupby('Content_Type')['Engagement_Rate'].mean().idxmax()
top_plat   = perf.groupby('Platform')['Bookings'].sum().idxmax()
low_ctb    = click_to_book.idxmin()

insights = [
    f'📌 Top Booking Theme: "{top_theme}" drives the most completed bookings — promotional content with a direct CTA converts best.',
    f'📌 Best Engagement Format: {top_format} achieves the highest average engagement rate — prioritise this format for awareness campaigns.',
    f'📌 Platform ROI: {top_plat} leads on total bookings. TikTok drives reach but low booking conversion — use it for top-of-funnel only.',
    f'📌 Click-to-Booking Gap: {low_ctb} has the lowest click-to-booking rate — landing page or checkout friction likely losing users after the click.',
    '📌 Unanswered Audience Need: Students and Young Professionals prefer Entertainment + Discounts but show low/moderate conversion — price or trust barrier remains.',
]
for i, text in enumerate(insights):
    fig.text(0.05, 0.245 - i * 0.022, text, fontsize=8.5, color='#333',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#fff3cd',
                       edgecolor='#f0ad4e', alpha=0.9))

# ── Recommendations ───────────────────────────────────────────────────────────
fig.text(0.05, 0.105, 'Strategic Recommendations', fontsize=12,
         fontweight='bold', color='#1a1a2e')
recs = [
    '1. Double down on Instagram Reels with Discount + Booking Guide themes — highest bookings per impression in the dataset.',
    '2. Use TikTok exclusively for awareness (Entertainment/Travel Hacks) — do not expect direct bookings; drive traffic to Instagram or site.',
    '3. Deprioritise X for content — lowest impressions, engagement, and bookings across all metrics. Limit to customer support replies only.',
    '4. Fix the post-click journey — high clicks on some posts are not converting to bookings, suggesting a friction point on the landing/checkout page.',
    '5. Create segment-specific content: Discount Reels for Students, Efficiency Carousels for Business, Trust/Testimonial posts for Families.',
]
for i, rec in enumerate(recs):
    fig.text(0.05, 0.088 - i * 0.018, rec, fontsize=8.5, color='#333')

plt.savefig('travler_week2_content_report.png', dpi=150, bbox_inches='tight', facecolor=BG)
print('Saved: travler_week2_content_report.png')
plt.show()
