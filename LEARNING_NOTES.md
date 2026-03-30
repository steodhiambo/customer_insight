# Travler Customer Insight — Full Learning Conversation

A complete record of the Week 1 analytics project walkthrough, covering how the
analysis was built, how segmentation works, how to solve any analytics problem,
and how to decide KPIs for a dashboard.

---

## Part 1 — The Project Brief

Travler has seen steady growth in website traffic but the increase has not
translated into a proportional rise in completed bookings. Amina K., the
Marketing Lead, explained that users are actively searching routes and comparing
prices but abandoning before payment. Brian O., the Head of Operations,
highlighted repeated customer inquiries about pricing inconsistencies and booking
confidence.

The task was to analyse a dataset of 20 users capturing search and booking
behaviour, identify patterns, build customer segments, and recommend targeted
actions for the marketing and operations teams.

---

## Part 2 — How the Project Was Solved From Start to Finish

### What Was in the File

The Excel file had one sheet with 20 rows — one row per user. Each row had 9
columns:

| Column | What It Captures |
|---|---|
| User_ID | Unique label per user |
| Age_Group | 18-24, 25-34, 35-44, 45+ |
| Travel_Purpose | Student, Business, Leisure, Family |
| Route_Searched | Nairobi-based route searched |
| Search_Frequency | How many times the user searched |
| Time_of_Search | Morning, Afternoon, Evening, Night |
| Device | Mobile or Desktop |
| Booking_Completed | Yes or No |
| Repeat_Visitor | Yes or No |

### The First Problem — The File Was Messy

Row 1 was a title. The actual column headers were on row 2. The file was loaded
with `header=1` to skip the title row. Search_Frequency was stored as text and
had to be converted to a number. A helper column called `Booked` (True/False)
was created from Booking_Completed (Yes/No) to make calculations cleaner.

### The Questions That Drove the Analysis

1. Out of 20 users, how many actually booked?
2. Does travel purpose affect whether someone books?
3. Does age matter?
4. Does device matter?
5. Does time of day matter?
6. Do people who search more times book more — or does high frequency mean hesitation?
7. Which routes are popular and are they converting?

### What the Numbers Said

- **Overall conversion: 45%** — 9 of 20 users booked
- **By travel purpose:** Family 100%, Business 83%, Leisure 20%, Student 0%
- **By age group:** 45+ converted 100%, 18-24 converted 0%
- **By device:** Desktop 86%, Mobile 23% — the biggest single gap in the data
- **By time of search:** Morning 83%, Afternoon 100%, Evening 0%, Night 0%
- **By search frequency:** Converters averaged 1.7 searches, non-converters averaged
  4.5 searches — more searching signals hesitation, not intent

### Building the Segments

Segments were built by combining multiple variables together, not just one.
The question was — which combination of characteristics predicts booking?

Four segments emerged:

| Segment | Age | Purpose | Device | Time | Searches | Conversion |
|---|---|---|---|---|---|---|
| Decisive Business Traveller | 25-44 | Business | Desktop | Morning | 1-3 | 83% |
| Family Planner | 45+ | Family | Mixed | Afternoon | 1 | 100% |
| Casual Leisure Browser | 25-44 | Leisure | Mobile | Evening | 2-3 | 20% |
| Price-Sensitive Student Searcher | 18-24 | Student | Mobile | Night | 5-7 | 0% |

### Building the Visual Report

The report was a single-page dashboard with 8 panels:

1. Pie chart — overall conversion rate
2. Horizontal bar — conversion by travel purpose
3. Vertical bar — conversion by age group
4. Horizontal bar — conversion by device
5. Vertical bar — conversion by time of search
6. Box plot — search frequency vs booking status
7. Segment profile table — all four segments side by side
8. Horizontal bar — route popularity with conversion overlay

Blue was used for high-converting categories, red for low-converting ones,
consistently across every chart. Insight callouts were written in plain language
below the charts. Five recommendations followed, each tied directly to a finding.

### The Five Recommendations

1. **Fix mobile checkout** — 76% of non-converters are on mobile. Simplify the
   payment flow and add trust signals.
2. **Retarget evening and night browsers** — 0% conversion at those times.
   Trigger a follow-up within 1 hour of an abandoned session.
3. **Unlock the student segment** — highest search frequency, 0% conversion.
   Introduce a student discount or pay-later option.
4. **Protect business and family users** — already converting at 83-100%.
   Keep the desktop experience frictionless and add loyalty perks.
5. **Add pricing transparency** — repeated searches on the same route signal
   price uncertainty. A Best Price Guarantee or fare-alert feature converts
   browsing into booking.

### The Overall Conclusion

Travler does not have a traffic problem. The problem is that the platform treats
all users the same when they are fundamentally different in their intent,
constraints, and readiness to book. The analysis gives the team a precise map of
where losses are happening and which fixes will have the biggest impact.

---

## Part 3 — Why Desktop Users Convert and Mobile Users Do Not

The website being the same is exactly the problem. The site was designed and
tested on desktop first. When that same site loads on mobile, the experience
degrades significantly.

### What Specifically Goes Wrong on Mobile

**1. The payment form is harder to fill in**
On desktop you have a full keyboard and easy navigation. On mobile you are
typing card numbers on a tiny keyboard. One mistake means starting again.

**2. Trust signals are harder to see**
Padlock icons and secure payment badges get pushed off screen on mobile.
Without seeing them, users feel unsafe entering card details.

**3. The screen is small so the process feels longer**
A 3-step process on desktop feels quick because you see everything at once.
On mobile each step fills the screen so the same process feels like 10 steps.

**4. Mobile users are in a distracted environment**
Desktop users sit at a desk, focused. Mobile users are on a bus, in bed, or
multitasking. A single interruption breaks the flow and they never return.

**5. Autofill works better on desktop**
Desktop browsers remember card details and fill them automatically. On
unoptimised mobile sites, autofill often fails and users type everything manually.

### The Simple Way to Think About It

Imagine filling in a paper form while wearing oven gloves. The form is exactly
the same. But the experience of completing it is completely different. That is
what mobile users face compared to desktop users.

### What Travler Needs to Do

- Larger tap targets for buttons
- Shorter, simpler payment form
- Visible trust signals that do not disappear on small screens
- Autofill support for card details
- A progress indicator so users know how close they are to finishing

---

## Part 4 — How to Segment Customers

### What Segmentation Is

Segmentation is dividing customers into groups where people inside each group
behave similarly to each other and differently from people in other groups. The
goal is not to label people — it is to understand that different people need
different things.

### The Wrong Way to Segment

Grouping by one variable only — age, gender, device. This gives you categories
but not insight. A 22 year old business analyst and a 22 year old student are
completely different customers even though they share the same age bracket.

### The Right Way to Segment

Combine multiple variables and look for groups that share a pattern across all
of them at the same time. The question is always — which combination of
characteristics predicts behaviour?

### How It Was Done for Travler Step by Step

**Step 1 — Start with the outcome**
The outcome was Booking_Completed. Everything else was about finding what
predicts it.

**Step 2 — Test each variable individually**
Each column was tested against the booking outcome one at a time to find which
variables matter.

**Step 3 — Look for combinations that cluster naturally**
Variables were combined to find which ones appeared together consistently. Every
student was 18-24, on mobile, searching at night, searching 5-7 times, and never
booked. That pattern repeating consistently across multiple variables is a segment.

**Step 4 — Name each segment by behaviour, not demographics**
The name describes what the person does and why — Decisive Business Traveller,
Price-Sensitive Student Searcher — not just who they are demographically.

**Step 5 — Validate that segments are meaningfully different**
100% conversion vs 0% conversion. 1 search vs 7 searches. Desktop morning vs
Mobile night. Differences that large justify treating each group completely
differently.

### The Three Tests of a Good Segment

**1. Is it distinct?** Does this group behave differently enough from the others?

**2. Is it actionable?** Can you do something different for this group? If a
segment does not change what you do, it has no value.

**3. Is it stable?** Does the pattern hold consistently or did it happen by
chance in this one dataset?

### The Simple Way to Think About It

Segmentation is like sorting your wardrobe. You could throw everything in one
pile and it technically works. But if you sort by type, by season, by occasion,
getting dressed becomes faster and you make better choices. Segmentation does
the same for your customers.

---

## Part 5 — A Universal Structure for Solving Any Analytics Problem

This structure applies to any analytics problem in any field — healthcare,
finance, education, retail, sport.

### Stage 1 — Understand the Business Problem First

Before touching any data, understand what the business is trying to solve.

Ask:
- What decision needs to be made?
- Who is making that decision?
- What would a good answer look like?
- What would change in the business if we knew the answer?

**If you do not understand the business problem you will answer the wrong
question perfectly.**

### Stage 2 — Understand Your Data

- What does each column represent?
- What is the outcome variable — the thing you are trying to explain?
- Are there quality issues — missing values, wrong data types, messy headers?
- How many rows do you have and is that enough to draw conclusions?

**Never assume the data is clean. Always look at it first.**

### Stage 3 — Define Your Questions

Turn the business problem into specific analytical questions. Good questions are:
- Specific — not "why don't people book" but "does device affect whether someone books"
- Answerable — you can answer it with the data you have
- Consequential — the answer will change something

**Write your questions down before you start. They are your roadmap.**

### Stage 4 — Analyse One Variable at a Time First

Take each variable and measure it against your outcome one at a time. This tells
you which variables matter and which do not.

**Do not jump to complex analysis before you know which variables are worth
investigating.**

### Stage 5 — Look for Combinations and Patterns

Combine variables that individually matter and look for patterns. This is where
real insight lives. This is how you go from "mobile users convert less" to
"young students on mobile at night searching 7 times never book because of price."

**Patterns that repeat across multiple variables are your most reliable findings.**

### Stage 6 — Interpret, Do Not Just Describe

Describing: mobile users convert at 23%.

Interpreting: mobile users convert at 23% because checkout friction and lack of
trust signals at the payment stage is blocking completion, and this is costing
Travler the majority of its potential bookings because 65% of users are on mobile.

Always ask — so what? Why does this number exist? What is causing it?

**Numbers without interpretation are just numbers.**

### Stage 7 — Segment Your Audience or Problem

In almost every analytics problem there are subgroups that behave differently.
Finding them is what allows targeted recommendations instead of generic ones.

### Stage 8 — Visualise for Your Audience

- Who will read this — analyst or executive?
- What is the single most important thing they need to see?
- Which chart type communicates this finding most clearly?

Rules:
- Use colour as a signal, not decoration
- Label charts so they can be read without explanation
- Put the most important finding first
- Write insight callouts in plain language

**A finding that cannot be communicated has no value.**

### Stage 9 — Recommend, Do Not Just Report

Every recommendation should follow this structure:

**Finding → Interpretation → Action**

Example:
- Finding — mobile converts at 23%
- Interpretation — checkout friction is blocking payment on mobile
- Action — simplify the mobile payment flow and add trust signals

**If your analysis does not end with clear actions it is an academic exercise,
not a business solution.**

### Stage 10 — Acknowledge the Limitations

- Is the sample size large enough to be confident?
- Could there be other explanations for what you found?
- What data do you not have that would make this stronger?

**Honesty about limitations makes your conclusions more credible, not less.**

### The Structure in One View

| Stage | Question You Are Answering |
|---|---|
| 1. Understand the problem | What decision needs to be made? |
| 2. Understand the data | What do I have to work with? |
| 3. Define your questions | What specifically am I trying to find out? |
| 4. Analyse individually | Which variables matter? |
| 5. Find combinations | What patterns emerge when variables combine? |
| 6. Interpret | Why do these numbers exist? So what? |
| 7. Segment | Who are the distinct groups and how do they differ? |
| 8. Visualise | How do I communicate this clearly to my audience? |
| 9. Recommend | What should the business actually do? |
| 10. Acknowledge limits | What can and cannot be concluded from this? |

### The One Thing to Remember

Every analytics problem in every field follows the same logic. You have an
outcome you care about. You have variables that might explain it. Your job is to
find which variables matter, how they combine, what they mean, and what should
be done about it. The field changes. The data changes. The structure never does.

---

## Part 6 — How to Decide KPIs for a Dashboard

### What a KPI Actually Is

KPI stands for Key Performance Indicator. The word that matters most is Key.
Not every metric is a KPI. A KPI is a metric that directly measures progress
towards a specific business goal.

The mistake most people make is putting every number they can calculate onto a
dashboard. That is not a dashboard, that is a data dump.

### The Starting Point — The Business Goal

Before deciding a single KPI, know what the business is trying to achieve.
The goal determines the KPIs, not the other way around.

Ask: **What does success look like for this business right now?**

| Business Goal | KPIs That Follow |
|---|---|
| Increase bookings | Conversion rate, booking completion rate, abandoned sessions |
| Grow the customer base | New users, acquisition cost, sign-up rate |
| Retain existing customers | Repeat booking rate, churn rate, loyalty uptake |
| Improve customer experience | Support ticket volume, resolution time, satisfaction score |
| Increase revenue | Average booking value, revenue per user, upsell rate |

### The Three Questions That Decide If Something Is a KPI

**1. Does it measure progress towards the business goal?**
If it does not connect to the goal it is not a KPI — it is background information.

**2. Can someone take action based on it?**
Every KPI should have an owner — a person or team responsible for moving it.
If nobody knows what to do when it changes, it is not a useful KPI.

**3. Does it change meaningfully over time?**
A metric that never moves is not useful to track. A KPI should reflect real
changes in the business.

### The Hierarchy of Metrics

**Level 1 — The North Star Metric**
The single most important number for the business. There should only be one.
For Travler it is the overall conversion rate.

**Level 2 — Primary KPIs**
The 3 to 5 metrics that directly drive the North Star. For Travler these were
conversion by device, by time of search, by travel purpose, and search frequency.

**Level 3 — Diagnostic Metrics**
Metrics that help you investigate when a primary KPI moves. Not on the main
dashboard but available when you need to dig deeper.

**Level 1 tells you what is happening. Level 2 tells you where. Level 3 tells
you why.**

### How to Decide What Goes on the Dashboard

**The So What Test**
If someone sees this number, what do they do with it? If the answer is nothing,
remove it.

**The Audience Test**
A CEO needs the North Star and top 3 KPIs. A marketing manager needs conversion
by segment. An operations manager needs route performance. Same data, different
dashboards for different audiences.

**The Clutter Test**
More than 7 to 9 metrics on a dashboard is too many. Cut ruthlessly. If it is
not essential, move it to a secondary view.

### A Practical Framework to Use Every Time

1. Write down the business goal in one sentence
2. Write down who will read the dashboard and what decision they need to make
3. Identify the one North Star metric
4. Identify 3 to 5 primary KPIs that explain what drives the North Star
5. For each KPI ask — can someone act on this? Does it connect to the goal? Does it change over time?
6. Remove anything that does not pass all three tests
7. Arrange so the North Star is seen first, primary KPIs second, diagnostic metrics accessible but not dominant

### The One Thing to Remember

A dashboard is not a collection of everything you can measure. It is a curated
view of the things that matter most to a specific person making a specific
decision. The discipline is not in adding metrics. It is in knowing what to
leave out.

---

## Summary

| Topic | Core Principle |
|---|---|
| Solving analytics problems | Understand the business goal before touching the data |
| Segmentation | Combine multiple variables — one variable gives categories, combinations give insight |
| Mobile vs Desktop gap | Same website, completely different experience — friction kills mobile conversion |
| KPIs | Every metric must connect to the goal, be actionable, and change meaningfully |
| Recommendations | Always follow Finding → Interpretation → Action |
| Dashboards | North Star first, primary KPIs second, diagnostic metrics third |
