# Travler Customer Insight Analysis — How It Was Done

---

## Overview

This document walks through every step taken to go from a raw Excel file to a
finished visual report covering customer behaviour, segments, and strategic
recommendations for the Travler marketing team.

---

## Step 1 — Exploring the File

The first thing done was checking what was actually inside the Excel file before
writing any analysis code. This involved:

- Listing the directory to confirm the file name
- Opening the Excel file and printing all sheet names
- Previewing the first few rows to understand the structure

**What was found:**
The file had one sheet called `Customer Data`. However, the first row was a
title (`Travler Digital Marketing Data - Customer Insight`) and the actual
column headers were sitting on the second row. This meant the data could not be
loaded directly — it needed a small fix.

---

## Step 2 — Loading and Cleaning the Data

Because the headers were on row 2 (not row 1), the file was loaded with
`header=1` in pandas, which tells it to skip the title row and treat row 2 as
the column names. After that, the first data row (which pandas had mistakenly
read as a header duplicate) was dropped.

One column — `Search_Frequency` — was stored as text in the Excel file, so it
was converted to a numeric type so it could be used in calculations.

A helper column called `Booked` (True/False) was also created from the
`Booking_Completed` column (Yes/No) to make grouping and percentage
calculations cleaner throughout the analysis.

**Final dataset: 20 users, 9 columns**

| Column | What it captures |
|---|---|
| User_ID | Unique identifier per user |
| Age_Group | 18-24, 25-34, 35-44, 45+ |
| Travel_Purpose | Student, Business, Leisure, Family |
| Route_Searched | The Nairobi-based route the user searched |
| Search_Frequency | How many times the user searched |
| Time_of_Search | Morning, Afternoon, Evening, Night |
| Device | Mobile or Desktop |
| Booking_Completed | Yes or No |
| Repeat_Visitor | Yes or No |

---

## Step 3 — Exploratory Analysis

Before building any visuals, a full breakdown of the data was run across every
dimension to understand what patterns existed. This was done by grouping the
data and calculating conversion rates (percentage of users who completed a
booking) for each category.

**What was calculated:**

- Overall conversion rate across all 20 users
- Conversion rate broken down by Travel Purpose
- Conversion rate broken down by Age Group
- Conversion rate broken down by Device
- Conversion rate broken down by Time of Search
- Average search frequency for users who booked vs those who did not
- Repeat visitor behaviour vs booking status
- Route popularity (how many users searched each route)

**Key numbers that came out of this:**

- Overall conversion: 45% (9 out of 20 users booked)
- Business travellers converted at 83%, Family at 100%
- Students converted at 0%, Leisure at 20%
- Desktop users converted at 86%, Mobile users at only 23%
- Morning and Afternoon searches converted at 83–100%
- Evening and Night searches converted at 0%
- Non-converters searched an average of 4.5 times vs 1.7 times for converters

These numbers told a clear story before a single chart was drawn.

---

## Step 4 — Identifying Customer Segments

With the patterns established, the next step was grouping users into meaningful
segments — not just by one variable like age, but by combining multiple
behavioural signals together (purpose + device + timing + frequency).

Four segments emerged naturally from the data:

**Segment 1 — Decisive Business Traveller**
- Age 25–44, Business purpose, Desktop, Morning searches, 1–3 searches
- 83% conversion rate
- These users know what they want, search once or twice, and book

**Segment 2 — Family Planner**
- Age 45+, Family purpose, Mixed device, Afternoon searches, 1 search
- 100% conversion rate
- The most reliable converters — they search once and commit

**Segment 3 — Casual Leisure Browser**
- Age 25–44, Leisure purpose, Mobile, Evening searches, 2–3 searches
- 20% conversion rate
- They are interested but not urgent — likely comparing options

**Segment 4 — Price-Sensitive Student Searcher**
- Age 18–24, Student purpose, Mobile, Night searches, 5–7 searches
- 0% conversion rate
- Highest engagement on the platform but never books — likely price-blocked

---

## Step 5 — Building the Visual Report

The report was built as a single large figure using matplotlib, divided into
8 panels plus a written insights and recommendations section at the bottom.

**Libraries used:**
- `pandas` — data loading, cleaning, and all calculations
- `matplotlib` — all charts and the final figure layout
- `matplotlib.patches` — used to draw the styled segment table cells

**How the layout was structured:**

The figure was set to 18 × 22 inches to give enough space for all panels.
Each chart panel was placed manually using `fig.add_axes([left, bottom, width, height])`
with fractional coordinates (0 to 1) so everything could be precisely positioned
without relying on a rigid grid.

**Chart by chart:**

1. **Overall Conversion (Pie chart)** — Simple split showing 45% booked vs 55%
   not booked. Chosen because it gives an immediate at-a-glance summary.

2. **Conversion by Travel Purpose (Horizontal bar)** — Horizontal bars were
   used because the category labels are long. Bars are coloured blue for
   high-converting segments and red for low-converting ones.

3. **Conversion by Age Group (Vertical bar)** — Age groups have a natural order
   (18-24 through 45+) so a vertical bar chart communicates the progression
   clearly.

4. **Conversion by Device (Horizontal bar)** — Same colour logic as purpose.
   The 86% vs 23% gap between Desktop and Mobile is one of the most important
   findings in the dataset.

5. **Conversion by Time of Search (Vertical bar)** — Time of day has a natural
   sequence (Morning → Afternoon → Evening → Night) so vertical bars in order
   show the pattern clearly.

6. **Search Frequency vs Booking (Box plot)** — A box plot was chosen here
   because it shows not just the average but the spread and distribution of
   search frequency for both groups. The average labels were added manually
   above each box for quick reading.

7. **Segment Behavioural Profile Table** — This was built entirely with
   matplotlib drawing primitives (text and FancyBboxPatch rectangles) rather
   than a standard chart. Each segment gets a colour-coded row showing all its
   key attributes side by side. Conversion rate cells are coloured blue or red
   to immediately signal high vs low performance.

8. **Route Popularity & Conversion (Horizontal bar)** — Shows how many users
   searched each route alongside the conversion rate for that route, giving
   operations a view of which routes are popular but underperforming.

**Colour scheme:**
- Blue (`#2E86AB`) = positive / converting
- Red (`#E84855`) = negative / not converting
- Amber background boxes = insight callouts
- Light grey page background for a clean, report-style look

---

## Step 6 — Insights and Recommendations

Below the charts, four key insight callouts were written directly onto the
figure using `fig.text()` with amber-coloured boxes to make them stand out.
These translate the numbers into plain-language observations.

Five strategic recommendations were then listed beneath the insights, each
mapped directly to a finding in the data:

1. Fix mobile checkout (device gap finding)
2. Retarget evening/night browsers (time of search finding)
3. Nurture the student segment (0% conversion + high frequency finding)
4. Protect business and family users (high conversion finding)
5. Add pricing transparency (high repeat search frequency finding)

---

## Step 7 — Saving the Output

The completed figure was saved as a high-resolution PNG file
(`travler_customer_insight_report.png`) at 150 DPI using `plt.savefig()` with
`bbox_inches='tight'` to ensure nothing was clipped at the edges.

---

## File Summary

| File | Purpose |
|---|---|
| `Travler Week 1 Customer Insight Dataset.xlsx` | Original raw data provided |
| `travler_customer_insight.py` | Full analysis and visualisation script |
| `travler_customer_insight_report.png` | Final output report image |
| `HOW_IT_WAS_DONE.md` | This document |

---

## Tools and Libraries

| Tool | Version requirement | Purpose |
|---|---|---|
| Python 3 | 3.8+ | Runtime |
| pandas | any recent | Data loading, cleaning, analysis |
| matplotlib | any recent | All charts and figure layout |
| openpyxl | any recent | Required by pandas to read .xlsx files |
