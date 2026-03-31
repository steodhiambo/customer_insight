from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

OUTPUT = "Travler_Week1_Customer_Insight_Submission.pdf"

BLUE  = colors.HexColor("#2E86AB")
RED   = colors.HexColor("#E84855")
AMBER = colors.HexColor("#F5A623")
LIGHT = colors.HexColor("#F4F6F8")
DARK  = colors.HexColor("#1A1A2E")

styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

title_style    = S("T",  fontSize=20, textColor=DARK,  leading=26, spaceAfter=4,  fontName="Helvetica-Bold")
sub_style      = S("Su", fontSize=11, textColor=BLUE,  leading=16, spaceAfter=2,  fontName="Helvetica")
h2_style       = S("H2", fontSize=13, textColor=DARK,  leading=18, spaceBefore=14, spaceAfter=4, fontName="Helvetica-Bold")
h3_style       = S("H3", fontSize=11, textColor=BLUE,  leading=16, spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
body_style     = S("B",  fontSize=10, textColor=DARK,  leading=15, spaceAfter=4,  fontName="Helvetica")
small_style    = S("Sm", fontSize=9,  textColor=colors.HexColor("#555555"), leading=13, fontName="Helvetica")
bold_body      = S("BB", fontSize=10, textColor=DARK,  leading=15, spaceAfter=4,  fontName="Helvetica-Bold")

def table_style(header_bg=BLUE):
    return TableStyle([
        ("BACKGROUND",  (0,0), (-1,0),  header_bg),
        ("TEXTCOLOR",   (0,0), (-1,0),  colors.white),
        ("FONTNAME",    (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[LIGHT, colors.white]),
        ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#CCCCCC")),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
    ])

def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm,  bottomMargin=2*cm
    )
    story = []
    W = A4[0] - 4*cm

    # ── HEADER ──────────────────────────────────────────────────────────────
    story += [
        Paragraph("Travler — Week 1 Customer Insight Analysis", title_style),
        Paragraph("Marketing Team Submission &nbsp;|&nbsp; Behavioural Analysis &amp; Segmentation", sub_style),
        HRFlowable(width=W, thickness=1.5, color=BLUE, spaceAfter=10),
    ]

    # ── 1. EXECUTIVE SUMMARY ────────────────────────────────────────────────
    story.append(Paragraph("1. Executive Summary", h2_style))
    story.append(Paragraph(
        "Travler does not have a traffic problem. The platform is attracting users who actively "
        "search routes and compare prices. The problem is conversion — only <b>45% of users "
        "(9 of 20) completed a booking</b>. The gap between traffic and bookings is explained by "
        "three compounding factors: mobile checkout friction, price uncertainty, and a mismatch "
        "between platform design and the behaviour of the platform's largest user groups.",
        body_style))

    kpi_data = [
        ["Metric", "Value", "Implication"],
        ["Overall Conversion Rate", "45%  (9 / 20 users)", "More than half of all users leave without booking"],
        ["Desktop Conversion",      "86%",                 "Desktop experience is working well"],
        ["Mobile Conversion",       "23%",                 "Mobile checkout is the single biggest drop-off point"],
        ["Morning / Afternoon Conv.","83 – 100%",          "Focused users in low-distraction windows convert reliably"],
        ["Evening / Night Conv.",   "0%",                  "Distracted browsing sessions never complete"],
        ["Avg. Searches — Converters",   "1.7",            "Low frequency = clear intent"],
        ["Avg. Searches — Non-converters","4.5",           "High frequency = price uncertainty and hesitation"],
    ]
    t = Table(kpi_data, colWidths=[W*0.38, W*0.22, W*0.40])
    t.setStyle(table_style())
    story += [Spacer(1, 6), t, Spacer(1, 4)]

    # ── 2. BEHAVIOURAL PATTERNS ─────────────────────────────────────────────
    story.append(Paragraph("2. Behavioural Patterns", h2_style))
    story.append(Paragraph(
        "The dataset was analysed across five dimensions — travel purpose, age group, device, "
        "time of search, and search frequency — to identify which factors consistently predict "
        "whether a user books or abandons.", body_style))

    story.append(Paragraph("2.1  Conversion by Travel Purpose", h3_style))
    purpose_data = [
        ["Travel Purpose", "Conversion Rate", "Interpretation"],
        ["Family",   "100%", "Committed, purposeful — searches once and books"],
        ["Business", "83%",  "Clear intent, time-sensitive, low tolerance for friction"],
        ["Leisure",  "20%",  "Interested but not urgent — comparing options"],
        ["Student",  "0%",   "Highest search volume on the platform, zero bookings"],
    ]
    t2 = Table(purpose_data, colWidths=[W*0.25, W*0.20, W*0.55])
    t2.setStyle(table_style())
    story += [t2, Spacer(1, 6)]

    story.append(Paragraph("2.2  Device Gap — The Biggest Single Finding", h3_style))
    story.append(Paragraph(
        "Desktop users convert at <b>86%</b>. Mobile users convert at <b>23%</b>. "
        "This is not a content or pricing problem — it is a checkout experience problem. "
        "The payment form is harder to complete on a small screen, trust signals disappear "
        "on mobile layouts, and any interruption during a mobile session results in permanent "
        "abandonment. The majority of non-converters (76%) are on mobile.", body_style))

    story.append(Paragraph("2.3  Time of Search", h3_style))
    time_data = [
        ["Time of Search", "Conversion Rate", "Context"],
        ["Morning",   "83%",  "Focused, intentional — likely at a desk"],
        ["Afternoon", "100%", "Peak conversion window — no distractions"],
        ["Evening",   "0%",   "Browsing from mobile in a distracted environment"],
        ["Night",     "0%",   "Late-night comparison shopping — never completes"],
    ]
    t3 = Table(time_data, colWidths=[W*0.22, W*0.20, W*0.58])
    t3.setStyle(table_style())
    story += [t3, Spacer(1, 6)]

    story.append(Paragraph("2.4  Search Frequency as a Hesitation Signal", h3_style))
    story.append(Paragraph(
        "Users who booked averaged <b>1.7 searches</b>. Users who did not book averaged "
        "<b>4.5 searches</b>. High search frequency does not signal growing intent — it signals "
        "that the user cannot find a reason to stop searching. The most common cause is price "
        "uncertainty: the user does not trust that the price they see is stable or the best "
        "available, so they keep checking. This is the same concern Brian O.'s support team "
        "is fielding on customer calls.", body_style))

    # ── 3. CUSTOMER SEGMENTS ────────────────────────────────────────────────
    story.append(Paragraph("3. Customer Segments", h2_style))
    story.append(Paragraph(
        "Four distinct behavioural segments were identified by combining travel purpose, device, "
        "time of search, and search frequency. Each segment has a consistent profile that repeats "
        "across multiple users in the dataset.", body_style))

    seg_data = [
        ["Segment", "Age", "Device", "Time", "Searches", "Conversion"],
        ["Decisive Business Traveller", "25–44", "Desktop", "Morning",   "1–3", "83%"],
        ["Family Planner",              "45+",   "Mixed",   "Afternoon", "1",   "100%"],
        ["Casual Leisure Browser",      "25–44", "Mobile",  "Evening",   "2–3", "20%"],
        ["Price-Sensitive Student",     "18–24", "Mobile",  "Night",     "5–7", "0%"],
    ]
    t4 = Table(seg_data, colWidths=[W*0.30, W*0.10, W*0.12, W*0.14, W*0.14, W*0.20])
    ts4 = table_style()
    ts4.add("TEXTCOLOR", (5,1), (5,2), BLUE)
    ts4.add("TEXTCOLOR", (5,3), (5,4), RED)
    ts4.add("FONTNAME",  (5,1), (5,4), "Helvetica-Bold")
    t4.setStyle(ts4)
    story += [t4, Spacer(1, 8)]

    segments = [
        ("Decisive Business Traveller — 83% conversion",
         "Knows the route, has a deadline, and books with minimal friction. "
         "Uses desktop in the morning. Searches 1–3 times before committing. "
         "Motivation: efficiency and reliability. Barrier: any friction in the checkout flow."),
        ("Family Planner — 100% conversion",
         "The most reliable converter on the platform. Searches once in the afternoon "
         "and commits immediately. Motivation: certainty and trust. "
         "Barrier: confusion or complexity in the booking process."),
        ("Casual Leisure Browser — 20% conversion",
         "Interested but not urgent. Browses on mobile in the evening while multitasking. "
         "Compares 2–3 options but rarely commits. Motivation: finding the best deal. "
         "Barrier: mobile checkout friction and no urgency trigger."),
        ("Price-Sensitive Student Searcher — 0% conversion",
         "The most active searcher on the platform — 5 to 7 searches per session — "
         "but never books. Uses mobile at night. Motivation: travel intent is real. "
         "Barrier: price is the hard block. No discount, no pay-later option, no booking."),
    ]
    for name, desc in segments:
        story.append(Paragraph(name, h3_style))
        story.append(Paragraph(desc, body_style))

    # ── 4. MOTIVATIONS AND BARRIERS ─────────────────────────────────────────
    story.append(Paragraph("4. Motivations and Barriers", h2_style))
    mb_data = [
        ["Factor",            "Motivations (drives booking)",          "Barriers (blocks booking)"],
        ["Device",            "Desktop: full keyboard, autofill, trust signals visible",
                              "Mobile: small screen, autofill fails, trust signals hidden"],
        ["Time of Search",    "Morning/Afternoon: focused, intentional sessions",
                              "Evening/Night: distracted environment, sessions abandoned"],
        ["Search Frequency",  "1–2 searches: clear intent, low uncertainty",
                              "5–7 searches: price uncertainty, no confidence mechanism"],
        ["Travel Purpose",    "Business/Family: clear need, deadline, or commitment",
                              "Student/Leisure: price-sensitive, no urgency, no trust anchor"],
        ["Pricing",           "Stable, transparent pricing builds confidence to book",
                              "Inconsistent or unclear pricing triggers repeat searching"],
    ]
    t5 = Table(mb_data, colWidths=[W*0.18, W*0.41, W*0.41])
    t5.setStyle(table_style())
    story += [t5, Spacer(1, 6)]

    # ── 5. RECOMMENDATIONS ──────────────────────────────────────────────────
    story.append(Paragraph("5. Recommendations", h2_style))
    recs = [
        ("1. Fix Mobile Checkout",
         "76% of non-converters are on mobile. Simplify the payment form, increase tap target "
         "sizes, enable autofill for card details, and ensure trust signals (padlock, secure "
         "badge) remain visible on small screens. Add a progress indicator so users know how "
         "close they are to completing the booking."),
        ("2. Retarget Evening and Night Abandoners",
         "Conversion at these times is 0%. Trigger an automated follow-up — push notification "
         "or email — within 1 hour of an abandoned session. The user had intent; they just "
         "did not complete in that window."),
        ("3. Unlock the Student Segment",
         "Students are the most active searchers on the platform with 0% conversion. "
         "A student discount or pay-later option directly removes the price barrier. "
         "This segment represents the largest untapped conversion opportunity."),
        ("4. Protect Business and Family Users",
         "These segments already convert at 83–100%. The priority is to keep the desktop "
         "experience frictionless and introduce loyalty perks (saved routes, priority booking) "
         "to increase repeat visits and lifetime value."),
        ("5. Add Pricing Transparency",
         "Repeated searches on the same route signal that users do not trust the price is "
         "stable. A Best Price Guarantee badge or fare-alert feature converts browsing into "
         "booking by removing the reason to keep searching. This also directly reduces the "
         "volume of pricing inquiries reaching Brian O.'s support team."),
    ]
    for title, body in recs:
        story.append(Paragraph(title, h3_style))
        story.append(Paragraph(body, body_style))

    # ── 6. CONCLUSION ───────────────────────────────────────────────────────
    story.append(Paragraph("6. Conclusion", h2_style))
    story.append(Paragraph(
        "Travler's growth challenge is not a traffic problem — it is a conversion problem "
        "concentrated in specific, identifiable segments and touchpoints. The data shows "
        "precisely where losses are happening: mobile checkout, evening and night sessions, "
        "the student segment, and price uncertainty at the point of decision. "
        "The five recommendations above are each tied directly to a finding in the data. "
        "Addressing them in order of impact — mobile first, then pricing transparency, "
        "then segment-specific interventions — gives the marketing and operations teams "
        "a clear, evidence-based roadmap for improving conversion without increasing "
        "traffic acquisition spend.", body_style))

    story += [
        Spacer(1, 10),
        HRFlowable(width=W, thickness=0.5, color=colors.HexColor("#CCCCCC"), spaceAfter=6),
        Paragraph(
            "Travler &nbsp;|&nbsp; Week 1 Customer Insight &nbsp;|&nbsp; "
            "Dataset: 20 users &nbsp;|&nbsp; Analysis: search &amp; booking behaviour",
            small_style),
    ]

    doc.build(story)
    print(f"Saved → {OUTPUT}")

if __name__ == "__main__":
    build()
