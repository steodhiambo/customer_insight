import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

# ── Load & clean ──────────────────────────────────────────────────────────────
xl = pd.ExcelFile('Travler Week 3 Campaign and Sentiment Dataset.xlsx')

camp = xl.parse('Campaign Performance', header=2)
camp.columns = ['Campaign_ID', 'Platform', 'Audience', 'Impressions',
                'Clicks', 'CTR', 'Cost_KES', 'Bookings', 'Conv_Rate']
camp = camp.dropna(subset=['Campaign_ID'])
for col in ['Impressions', 'Clicks', 'CTR', 'Cost_KES', 'Bookings', 'Conv_Rate']:
    camp[col] = pd.to_numeric(camp[col])
camp['CPA'] = camp['Cost_KES'] / camp['Bookings']          # cost per acquisition
camp['CPM'] = camp['Cost_KES'] / camp['Impressions'] * 1000  # cost per 1k impressions

sent = xl.parse('Customer Sentiment', header=1)
sent.columns = ['Comment_ID', 'Platform', 'Sentiment', 'Theme', 'Comment_Summary']
sent = sent.dropna(subset=['Comment_ID'])

# ── Palette ───────────────────────────────────────────────────────────────────
BG = '#F8F9FA'
PLAT_COLORS = {'Instagram': '#E1306C', 'TikTok': '#010101',
               'X': '#1DA1F2', 'Google Ads': '#4285F4'}
SENT_COLORS = {'Positive': '#3BB273', 'Neutral': '#F4A261', 'Negative': '#E84855'}
HIGH = '#3BB273'; LOW = '#E84855'; MID = '#F4A261'

fig = plt.figure(figsize=(18, 24), facecolor=BG)
fig.suptitle('Travler – Week 3 Campaign Performance & Sentiment Report',
             fontsize=20, fontweight='bold', y=0.985, color='#1a1a2e')

positions = [
    (0.05, 0.76, 0.27, 0.18),   # 1 – conversion rate by channel
    (0.37, 0.76, 0.27, 0.18),   # 2 – bookings vs cost by channel
    (0.69, 0.76, 0.26, 0.18),   # 3 – CTR by audience
    (0.05, 0.52, 0.27, 0.18),   # 4 – cost per acquisition
    (0.37, 0.52, 0.27, 0.18),   # 5 – sentiment breakdown (stacked bar)
    (0.69, 0.52, 0.26, 0.18),   # 6 – sentiment theme frequency
    (0.05, 0.28, 0.90, 0.18),   # 7 – campaign summary table
]
axes = [fig.add_axes(p, facecolor=BG) for p in positions]

def style(ax, title):
    ax.set_title(title, fontsize=11, fontweight='bold', color='#1a1a2e', pad=8)
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(colors='#444')
    for sp in ['left', 'bottom']:
        ax.spines[sp].set_color('#ccc')

# ── 1. Conversion rate by platform ───────────────────────────────────────────
ax = axes[0]
plat_conv = camp.groupby('Platform')['Conv_Rate'].mean().sort_values()
colors = [PLAT_COLORS.get(p, '#999') for p in plat_conv.index]
bars = ax.barh(plat_conv.index, plat_conv.values, color=colors, edgecolor='white')
for bar, val in zip(bars, plat_conv.values):
    ax.text(val + 0.2, bar.get_y() + bar.get_height() / 2,
            f'{val:.1f}%', va='center', fontsize=9, color='#333')
ax.set_xlabel('Avg Conversion Rate (%)', fontsize=8, color='#555')
style(ax, 'Avg Conversion Rate by Platform')

# ── 2. Total bookings vs total cost by platform ───────────────────────────────
ax = axes[1]
plat_bc = camp.groupby('Platform')[['Bookings', 'Cost_KES']].sum()
x = range(len(plat_bc))
w = 0.35
ax.bar([i - w/2 for i in x], plat_bc['Bookings'],
       width=w, color=[PLAT_COLORS.get(p, '#999') for p in plat_bc.index],
       edgecolor='white', label='Bookings')
ax2 = ax.twinx()
ax2.bar([i + w/2 for i in x], plat_bc['Cost_KES'] / 1000,
        width=w, color='#aaa', edgecolor='white', alpha=0.7, label='Cost (KES 000s)')
ax.set_xticks(list(x)); ax.set_xticklabels(plat_bc.index, fontsize=8)
ax.set_ylabel('Total Bookings', fontsize=8, color='#333')
ax2.set_ylabel('Cost (KES 000s)', fontsize=8, color='#888')
ax.spines[['top', 'right']].set_visible(False)
ax2.spines[['top']].set_visible(False)
handles = [mpatches.Patch(color='#4285F4', label='Bookings'),
           mpatches.Patch(color='#aaa', label='Cost (KES 000s)')]
ax.legend(handles=handles, fontsize=7, loc='upper left')
ax.set_title('Total Bookings vs Spend by Platform', fontsize=11,
             fontweight='bold', color='#1a1a2e', pad=8)

# ── 3. CTR by audience segment ────────────────────────────────────────────────
ax = axes[2]
aud_ctr = camp.groupby('Audience')['CTR'].mean().sort_values()
colors = [HIGH if v >= aud_ctr.median() else LOW for v in aud_ctr]
bars = ax.barh(aud_ctr.index, aud_ctr.values, color=colors, edgecolor='white')
for bar, val in zip(bars, aud_ctr.values):
    ax.text(val + 0.05, bar.get_y() + bar.get_height() / 2,
            f'{val:.1f}%', va='center', fontsize=9, color='#333')
ax.set_xlabel('Avg CTR (%)', fontsize=8, color='#555')
style(ax, 'Avg CTR by Audience Segment')

# ── 4. Cost per acquisition (CPA) by campaign ────────────────────────────────
ax = axes[3]
cpa = camp.set_index('Campaign_ID')['CPA'].sort_values()
colors = [HIGH if v <= cpa.median() else LOW for v in cpa]
bars = ax.barh(cpa.index, cpa.values, color=colors, edgecolor='white')
for bar, val in zip(bars, cpa.values):
    ax.text(val + 5, bar.get_y() + bar.get_height() / 2,
            f'KES {val:.0f}', va='center', fontsize=8, color='#333')
ax.set_xlabel('Cost per Acquisition (KES)', fontsize=8, color='#555')
ax.axvline(cpa.median(), color='#888', linestyle='--', linewidth=1, label=f'Median: KES {cpa.median():.0f}')
ax.legend(fontsize=7)
style(ax, 'Cost per Acquisition by Campaign  (lower = better)')

# ── 5. Sentiment breakdown by platform ───────────────────────────────────────
ax = axes[4]
sent_plat = sent.groupby(['Platform', 'Sentiment']).size().unstack(fill_value=0)
for col in ['Positive', 'Neutral', 'Negative']:
    if col not in sent_plat.columns:
        sent_plat[col] = 0
sent_plat = sent_plat[['Positive', 'Neutral', 'Negative']]
bottom = [0] * len(sent_plat)
for sentiment in ['Positive', 'Neutral', 'Negative']:
    vals = sent_plat[sentiment].values
    bars = ax.bar(sent_plat.index, vals, bottom=bottom,
                  color=SENT_COLORS[sentiment], edgecolor='white', label=sentiment)
    bottom = [b + v for b, v in zip(bottom, vals)]
ax.set_ylabel('Comment Count', fontsize=8, color='#555')
ax.legend(fontsize=7, loc='upper right')
style(ax, 'Sentiment Distribution by Platform')

# ── 6. Sentiment theme frequency ─────────────────────────────────────────────
ax = axes[5]
theme_sent = sent.groupby(['Theme', 'Sentiment']).size().unstack(fill_value=0)
theme_total = theme_sent.sum(axis=1).sort_values(ascending=True)
colors = []
for theme in theme_total.index:
    row = theme_sent.loc[theme] if theme in theme_sent.index else {}
    neg = row.get('Negative', 0)
    pos = row.get('Positive', 0)
    colors.append(LOW if neg > pos else HIGH if pos > 0 else MID)
bars = ax.barh(theme_total.index, theme_total.values, color=colors, edgecolor='white')
for bar, val in zip(bars, theme_total.values):
    ax.text(val + 0.05, bar.get_y() + bar.get_height() / 2,
            str(int(val)), va='center', fontsize=9, color='#333')
ax.set_xlabel('Mentions', fontsize=8, color='#555')
style(ax, 'Sentiment Themes — Frequency & Tone')

# ── 7. Campaign summary table ─────────────────────────────────────────────────
ax = axes[6]
ax.axis('off')
cols = ['Campaign', 'Platform', 'Audience', 'Impressions', 'Clicks',
        'CTR (%)', 'Bookings', 'Conv Rate (%)', 'CPA (KES)']
col_keys = ['Campaign_ID', 'Platform', 'Audience', 'Impressions', 'Clicks',
            'CTR', 'Bookings', 'Conv_Rate', 'CPA']
col_widths = [0.7, 1.0, 1.5, 1.1, 0.8, 0.7, 0.8, 1.1, 1.0]
total_w = sum(col_widths)
ax.set_xlim(0, total_w); ax.set_ylim(0, len(camp) + 1)

x_pos = 0
for col, w in zip(cols, col_widths):
    ax.text(x_pos + w / 2, len(camp) + 0.4, col,
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1a1a2e')
    x_pos += w

row_colors = ['#d4edda', '#fff3cd', '#f8d7da', '#d1ecf1',
              '#d4edda', '#d4edda', '#fff3cd', '#f8d7da']
for i, row in camp.reset_index(drop=True).iterrows():
    y = len(camp) - 1 - i
    rect = mpatches.FancyBboxPatch((0, y + 0.05), total_w, 0.88,
                                    boxstyle='round,pad=0.02',
                                    facecolor=row_colors[i % len(row_colors)] + 'aa',
                                    edgecolor='#ccc', linewidth=0.8)
    ax.add_patch(rect)
    x_pos = 0
    for key, w in zip(col_keys, col_widths):
        val = row[key]
        if key in ['Impressions', 'Clicks', 'Cost_KES']:
            txt = f'{int(val):,}'
        elif key == 'CPA':
            txt = f'{val:.0f}'
        elif key in ['CTR', 'Conv_Rate']:
            txt = f'{float(val):.1f}%'
        else:
            txt = str(val)
        ax.text(x_pos + w / 2, y + 0.5, txt,
                ha='center', va='center', fontsize=8, color='#1a1a2e')
        x_pos += w

ax.set_title('Full Campaign Summary Table', fontsize=11,
             fontweight='bold', color='#1a1a2e', pad=8)

# ── Key insights ──────────────────────────────────────────────────────────────
best_conv   = camp.loc[camp['Conv_Rate'].idxmax()]
worst_conv  = camp.loc[camp['Conv_Rate'].idxmin()]
best_cpa    = camp.loc[camp['CPA'].idxmin()]
neg_pct     = (sent['Sentiment'] == 'Negative').mean() * 100
top_neg_theme = sent[sent['Sentiment'] == 'Negative']['Theme'].value_counts().idxmax()

insights = [
    f'📌 Top Performer: {best_conv["Platform"]} ({best_conv["Audience"]}) — {best_conv["Conv_Rate"]:.1f}% conversion rate, '
    f'lowest CPA at KES {best_cpa["CPA"]:.0f}. High-intent audience + search-based targeting drives results.',

    f'📌 Underperformer: TikTok (both audiences) — only {worst_conv["Conv_Rate"]:.1f}% conversion despite highest impressions (40k). '
    f'Strong reach, weak intent. Use for awareness only, not conversion.',

    f'📌 Google Ads Efficiency: Highest conversion rates (12–15.7%) across both audience segments. '
    f'Search intent targeting outperforms social media for direct bookings.',

    f'📌 Sentiment Alert: {neg_pct:.0f}% of customer comments are Negative. '
    f'Top concern: "{top_neg_theme}" — directly linked to the recent viral complaint incident.',

    '📌 Trust Gap: X (Twitter) carries the most negative sentiment (Trust + Payment themes). '
    'Reputational damage is concentrated here — priority platform for crisis response.',
]
for i, text in enumerate(insights):
    fig.text(0.05, 0.245 - i * 0.022, text, fontsize=8.5, color='#333',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#fff3cd',
                       edgecolor='#f0ad4e', alpha=0.9))

# ── Recommendations ───────────────────────────────────────────────────────────
recs = [
    '✅ Rec 1 — Shift budget from TikTok to Google Ads: TikTok delivers reach but not bookings. '
    'Reallocate 20–30% of TikTok spend to Google Ads where conversion rates are 8–10× higher.',

    '✅ Rec 2 — Crisis response on X: Publish a public acknowledgement post addressing the payment/trust complaints. '
    'Pin a clear refund & support policy. Respond to every negative comment within 2 hours.',

    '✅ Rec 3 — Retarget high-CTR audiences: Students and Young Professionals click but don\'t convert. '
    'Deploy a retargeting sequence (discount offer + trust badge) within 24 hours of a click with no booking.',
]
for i, text in enumerate(recs):
    fig.text(0.05, 0.135 - i * 0.030, text, fontsize=8.5, color='#1a1a2e',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#d4edda',
                       edgecolor='#28a745', alpha=0.9))

plt.savefig('travler_week3_campaign_sentiment_report.png',
            dpi=150, bbox_inches='tight', facecolor=BG)
print('Saved: travler_week3_campaign_sentiment_report.png')
