# Travler — Customer Insight Analysis (Week 1)

A behavioural analysis of Travler's customer search and booking data, built to help the marketing team understand who their users are, how they behave on the platform, and what is driving or blocking conversions.

---

## Background

Travler has seen steady growth in website traffic but the increase has not translated into a proportional rise in completed bookings. This project analyses a dataset of 20 users across a recent period to surface patterns in search behaviour, identify distinct customer segments, and recommend targeted actions for the marketing and operations teams.

---

## Files

| File | Description |
|---|---|
| `Travler Week 1 Customer Insight Dataset.xlsx` | Raw dataset provided by the Travler team |
| `travler_customer_insight.py` | Full analysis and visualisation script |
| `travler_customer_insight_report.png` | Final output — single-page visual report |
| `HOW_IT_WAS_DONE.md` | Step-by-step walkthrough of the entire analysis |
| `README.md` | This file |

---

## What the Analysis Covers

- Overall conversion rate across all users
- Conversion breakdown by travel purpose, age group, device, and time of search
- Search frequency comparison between users who booked and those who did not
- Route popularity with conversion overlay
- Four behavioural customer segments with full profiles

---

## Customer Segments Identified

| Segment | Conversion Rate | Key Signals |
|---|---|---|
| Decisive Business Traveller | 83% | Desktop, morning, 1–3 searches |
| Family Planner | 100% | Afternoon, single search, commits immediately |
| Casual Leisure Browser | 20% | Mobile, evening, comparison shopping |
| Price-Sensitive Student Searcher | 0% | Mobile, night, 5–7 searches, never books |

---

## Key Findings

- **45%** overall conversion rate (9 of 20 users booked)
- Desktop users convert at **86%** vs Mobile at **23%** — the biggest single gap in the data
- Morning and Afternoon searches convert at **83–100%**; Evening and Night searches convert at **0%**
- Non-converters search an average of **4.5×** vs **1.7×** for converters — high frequency signals hesitation, not intent
- Students and Leisure users make up **55% of searches** but contribute almost nothing to bookings

---

## Recommendations

1. **Fix mobile checkout** — simplify the payment flow and add trust signals for mobile users
2. **Retarget evening/night browsers** — trigger follow-up within 1 hour of an abandoned session
3. **Nurture the student segment** — introduce a student discount or pay-later option to unlock 0% conversion
4. **Protect business and family users** — prioritise a frictionless desktop experience and loyalty perks
5. **Add pricing transparency** — a Best Price Guarantee or fare-alert feature to reduce repeat searching without booking

---

## How to Run

```bash
# Install dependencies
pip install pandas matplotlib openpyxl

# Run the analysis
python3 travler_customer_insight.py
```

The script will generate `travler_customer_insight_report.png` in the same directory.

---

## Requirements

- Python 3.8+
- pandas
- matplotlib
- openpyxl
