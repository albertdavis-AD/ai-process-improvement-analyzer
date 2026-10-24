
from __future__ import annotations

from io import BytesIO
import html
import math

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)


# ============================================================
# FLOWMIND AI | PROCESS INTELLIGENCE & OPTIMIZATION
# ============================================================

st.set_page_config(
    page_title="FLOWMIND AI | Process Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_VERSION = "3.0"

REQUIRED_COLUMNS = [
    "process_step",
    "avg_work_hours",
    "avg_wait_hours",
    "avg_cost_inr",
    "rework_rate_pct",
    "activity_type",
]

NUMERIC_COLUMNS = [
    "avg_work_hours",
    "avg_wait_hours",
    "avg_cost_inr",
    "rework_rate_pct",
]

NAV_ITEMS = [
    "Executive Overview",
    "What-If Analysis",
    "Recommendations",
    "Management Report",
    "Detailed Process Data",
]

COLORS = {
    "navy": "#10172A",
    "navy2": "#17233D",
    "blue": "#4776F5",
    "cyan": "#35C6D8",
    "teal": "#17B897",
    "purple": "#9B7BFA",
    "orange": "#F2A65A",
    "red": "#E66B78",
    "text": "#17233D",
    "muted": "#66758C",
    "border": "#E4EAF3",
    "surface": "#FFFFFF",
    "background": "#F4F7FC",
}


# ============================================================
# VISUAL DESIGN
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #F4F7FC;
        color: #17233D;
    }

    [data-testid="stHeader"] {
        background: rgba(244,247,252,0.92);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #10172A 0%, #17233D 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stSidebar"] * {
        color: #EAF0FF;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
        background: rgba(255,255,255,0.06);
        border: 1px dashed #6C83B1;
        border-radius: 12px;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {
        color: #EAF0FF !important;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
        background: #4776F5 !important;
        border: 0 !important;
        color: white !important;
        border-radius: 8px !important;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploader"] small {
        color: #B9C7E5 !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 7px 8px;
        border-radius: 8px;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: rgba(255,255,255,0.07);
    }

    h1, h2, h3 {
        font-family: 'Manrope', sans-serif !important;
        letter-spacing: -0.6px;
    }

    h1 {
        color: #10172A !important;
        font-weight: 800 !important;
    }

    h2, h3 {
        color: #17233D !important;
        font-weight: 700 !important;
    }

    .brand {
        padding: 14px 4px 22px 4px;
    }

    .brand-mark {
        display: inline-block;
        background: linear-gradient(135deg, #4776F5, #35C6D8);
        color: white;
        font-size: 23px;
        font-weight: 800;
        padding: 9px 13px;
        border-radius: 13px;
        margin-bottom: 12px;
        box-shadow: 0 8px 24px rgba(71,118,245,0.25);
    }

    .brand-title {
        font-family: 'Manrope', sans-serif;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: 1.3px;
        color: #FFFFFF;
    }

    .brand-subtitle {
        color: #9FB1D5;
        font-size: 11px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 5px;
    }

    .eyebrow {
        font-size: 11px;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        color: #4776F5;
        font-weight: 800;
        margin-bottom: 7px;
    }

    .page-subtitle {
        color: #66758C;
        font-size: 14px;
        margin-top: -6px;
        margin-bottom: 22px;
        line-height: 1.6;
    }

    .hero {
        background: linear-gradient(120deg, #10172A 0%, #1B3155 68%, #235A77 100%);
        padding: 27px 30px;
        border-radius: 19px;
        color: white;
        margin: 4px 0 23px 0;
        box-shadow: 0 12px 32px rgba(16,23,42,0.12);
    }

    .hero-kicker {
        color: #8DE4E5;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 9px;
    }

    .hero-title {
        color: white;
        font-family: 'Manrope', sans-serif;
        font-size: 29px;
        font-weight: 800;
        line-height: 1.25;
        margin-bottom: 10px;
    }

    .hero-copy {
        color: #D0DCF2;
        font-size: 13px;
        line-height: 1.7;
        max-width: 780px;
    }

    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E4EAF3;
        border-radius: 15px;
        padding: 18px 19px;
        min-height: 126px;
        box-shadow: 0 4px 14px rgba(28,46,79,0.035);
    }

    .metric-label {
        color: #66758C;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }

    .metric-value {
        color: #10172A;
        font-family: 'Manrope', sans-serif;
        font-size: 27px;
        font-weight: 800;
        line-height: 1.2;
    }

    .metric-note {
        color: #738198;
        font-size: 11px;
        margin-top: 9px;
        line-height: 1.45;
    }

    .section-heading {
        font-family: 'Manrope', sans-serif;
        font-size: 18px;
        font-weight: 800;
        color: #17233D;
        margin: 7px 0 5px 0;
    }

    .section-copy {
        color: #738198;
        font-size: 12px;
        margin-bottom: 13px;
        line-height: 1.6;
    }

    .insight-card {
        background: #FFFFFF;
        border: 1px solid #E4EAF3;
        border-left: 4px solid #4776F5;
        border-radius: 12px;
        padding: 15px 16px;
        margin-bottom: 10px;
    }

    .insight-title {
        font-size: 13px;
        font-weight: 800;
        color: #17233D;
        margin-bottom: 5px;
    }

    .insight-copy {
        color: #66758C;
        font-size: 12px;
        line-height: 1.65;
    }

    .demo-pill {
        display: inline-block;
        color: #79521A;
        background: #FFF2D9;
        border: 1px solid #F5DDAA;
        border-radius: 30px;
        padding: 5px 10px;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.6px;
    }

    .live-pill {
        display: inline-block;
        color: #13785F;
        background: #E0F7EF;
        border: 1px solid #B5EAD9;
        border-radius: 30px;
        padding: 5px 10px;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.6px;
    }

    .footer {
        border-top: 1px solid #E1E7F0;
        margin-top: 38px;
        padding: 15px 0 8px 0;
        color: #8290A5;
        font-size: 10px;
        letter-spacing: 0.3px;
    }

    div[data-testid="stDownloadButton"] button,
    div[data-testid="stButton"] button {
        border-radius: 9px;
        font-weight: 700;
        min-height: 40px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #E4EAF3;
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-testid="stPlotlyChart"] {
        background: white;
        border: 1px solid #E4EAF3;
        border-radius: 14px;
        padding: 7px;
    }

    @media (max-width: 768px) {
        .hero-title { font-size: 23px; }
        .metric-value { font-size: 23px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DEMONSTRATION DATA
# ============================================================

def sample_data() -> pd.DataFrame:
    return pd.DataFrame({
        "process_step": [
            "Application Submission",
            "Document Verification",
            "Credit Check",
            "Risk Review",
            "Final Approval",
            "Disbursement",
        ],
        "avg_work_hours": [0.5, 2.0, 1.0, 3.0, 1.5, 1.0],
        "avg_wait_hours": [1.0, 12.0, 5.0, 18.0, 10.0, 4.0],
        "avg_cost_inr": [100, 350, 250, 600, 300, 200],
        "rework_rate_pct": [2, 15, 5, 12, 4, 3],
        "activity_type": [
            "Digital", "Manual", "Automated",
            "Manual", "Manual", "Automated",
        ],
    })


# ============================================================
# DATA VALIDATION
# ============================================================

def validate_data(raw: pd.DataFrame) -> tuple[pd.DataFrame | None, list[str]]:
    df = raw.copy()
    errors = []

    df.columns = [str(c).strip().lower() for c in df.columns]

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        return None, [
            "Missing required columns: " + ", ".join(missing)
        ]

    df = df[REQUIRED_COLUMNS].copy()

    if df.empty:
        return None, ["The uploaded file contains no data rows."]

    df["process_step"] = df["process_step"].fillna("").astype(str).str.strip()
    df["activity_type"] = df["activity_type"].fillna("").astype(str).str.strip()

    if (df["process_step"] == "").any():
        errors.append("Every row must have a process_step value.")

    if (df["activity_type"] == "").any():
        errors.append("Every row must have an activity_type value.")

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")
        if df[column].isna().any():
            errors.append(
                f"Column '{column}' contains blank or non-numeric values."
            )

    if errors:
        return None, errors

    for column in ["avg_work_hours", "avg_wait_hours", "avg_cost_inr"]:
        if (df[column] < 0).any():
            errors.append(f"Column '{column}' cannot contain negative values.")

    if not df["rework_rate_pct"].between(0, 100).all():
        errors.append("rework_rate_pct must be between 0 and 100.")

    if errors:
        return None, errors

    df["activity_type"] = df["activity_type"].str.title()

    return df.reset_index(drop=True), []


# ============================================================
# ANALYTICS AND BUSINESS LOGIC
# ============================================================

def calculate_metrics(df: pd.DataFrame) -> dict:
    total_work = float(df["avg_work_hours"].sum())
    total_wait = float(df["avg_wait_hours"].sum())
    total_cost = float(df["avg_cost_inr"].sum())
    total_time = total_work + total_wait

    manual_mask = df["activity_type"].str.lower().eq("manual")
    manual_share = (
        float(manual_mask.mean() * 100) if len(df) else 0.0
    )

    weighted_rework = float(df["rework_rate_pct"].mean()) if len(df) else 0.0
    wait_share = total_wait / total_time * 100 if total_time > 0 else 0.0

    return {
        "total_work": total_work,
        "total_wait": total_wait,
        "total_time": total_time,
        "total_cost": total_cost,
        "manual_share": manual_share,
        "avg_rework": weighted_rework,
        "wait_share": wait_share,
    }


def build_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    records = []

    max_wait = max(float(df["avg_wait_hours"].max()), 1.0)
    max_work = max(float(df["avg_work_hours"].max()), 1.0)
    max_rework = max(float(df["rework_rate_pct"].max()), 1.0)
    max_cost = max(float(df["avg_cost_inr"].max()), 1.0)

    for _, row in df.iterrows():
        wait = float(row["avg_wait_hours"])
        work = float(row["avg_work_hours"])
        rework = float(row["rework_rate_pct"])
        cost = float(row["avg_cost_inr"])
        activity = str(row["activity_type"]).lower()

        # Transparent heuristic score, not a trained AI prediction.
        score = (
            35 * wait / max_wait
            + 25 * rework / max_rework
            + 20 * work / max_work
            + 10 * cost / max_cost
            + (10 if activity == "manual" else 3 if activity == "digital" else 0)
        )
        score = min(100.0, score)

        reasons = []
        actions = []

        if wait >= 8:
            reasons.append(f"High waiting time ({wait:.1f} hours)")
            actions.append("Review queue ownership, handoffs, and service-level targets")

        if rework >= 10:
            reasons.append(f"Elevated rework ({rework:.1f}%)")
            actions.append("Introduce validation checks, clearer standards, and root-cause review")

        if activity == "manual":
            reasons.append("Manual activity")
            actions.append("Assess rule-based automation or assisted data entry")

        if work >= 2:
            reasons.append(f"High work effort ({work:.1f} hours)")
            actions.append("Break down the task and remove duplicated steps")

        if not reasons:
            reasons.append("No major threshold breach detected")
            actions.append("Monitor performance and preserve the current control")

        if score >= 65:
            priority = "High"
        elif score >= 40:
            priority = "Medium"
        else:
            priority = "Low"

        unique_actions = list(dict.fromkeys(actions))

        records.append({
            "process_step": row["process_step"],
            "priority": priority,
            "opportunity_score": round(score, 1),
            "activity_type": row["activity_type"],
            "avg_wait_hours": wait,
            "rework_rate_pct": rework,
            "avg_cost_inr": cost,
            "key_signals": "; ".join(reasons),
            "recommended_action": "; ".join(unique_actions),
        })

    result = pd.DataFrame(records)
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    result["_order"] = result["priority"].map(priority_order)
    return (
        result.sort_values(
            ["_order", "opportunity_score"],
            ascending=[True, False],
        )
        .drop(columns="_order")
        .reset_index(drop=True)
    )


def format_inr(value: float) -> str:
    return f"₹{value:,.0f}"


def make_chart_layout(fig, height=330):
    fig.update_layout(
        height=height,
        margin=dict(l=18, r=18, t=35, b=18),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="DM Sans, sans-serif", color="#66758C", size=11),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
    )
    fig.update_xaxes(showgrid=False, linecolor="#E4EAF3")
    fig.update_yaxes(
        gridcolor="#EEF2F8",
        zerolinecolor="#E4EAF3",
        linecolor="#E4EAF3",
    )
    return fig


# ============================================================
# PDF REPORT GENERATOR
# ============================================================

def generate_pdf(
    df: pd.DataFrame,
    recs: pd.DataFrame,
    metrics: dict,
    scenario: dict | None = None,
) -> bytes:
    buffer = BytesIO()
    page_size = landscape(A4)

    doc = SimpleDocTemplate(
        buffer,
        pagesize=page_size,
        rightMargin=1.25 * cm,
        leftMargin=1.25 * cm,
        topMargin=1.35 * cm,
        bottomMargin=1.35 * cm,
        title="FLOWMIND AI - Process Intelligence Report",
        author="FLOWMIND AI",
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="FMTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=27,
        textColor=colors.HexColor("#10172A"),
        alignment=TA_LEFT,
        spaceAfter=7,
    ))
    styles.add(ParagraphStyle(
        name="FMSubtitle",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#66758C"),
        spaceAfter=13,
    ))
    styles.add(ParagraphStyle(
        name="FMHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#17233D"),
        spaceBefore=10,
        spaceAfter=7,
    ))
    styles.add(ParagraphStyle(
        name="FMCell",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#26354D"),
        wordWrap="CJK",
    ))
    styles.add(ParagraphStyle(
        name="FMCellBold",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=7.2,
        leading=9.2,
        textColor=colors.white,
    ))
    styles.add(ParagraphStyle(
        name="FMBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#34445D"),
        spaceAfter=7,
    ))

    story = []

    story.append(Paragraph("FLOWMIND AI", styles["FMTitle"]))
    story.append(Paragraph(
        "PROCESS INTELLIGENCE &amp; OPTIMIZATION | MANAGEMENT REPORT",
        styles["FMSubtitle"],
    ))
    story.append(Paragraph(
        "A data-driven review of process performance, operational friction, "
        "and potential improvement opportunities.",
        styles["FMBody"],
    ))

    summary_data = [
        [
            Paragraph("<b>Total modeled time</b>", styles["FMCell"]),
            Paragraph("<b>Waiting time</b>", styles["FMCell"]),
            Paragraph("<b>Modeled step cost</b>", styles["FMCell"]),
            Paragraph("<b>Manual activity share</b>", styles["FMCell"]),
        ],
        [
            Paragraph(f"{metrics['total_time']:,.1f} hrs", styles["FMCell"]),
            Paragraph(f"{metrics['total_wait']:,.1f} hrs", styles["FMCell"]),
            Paragraph(format_inr(metrics["total_cost"]), styles["FMCell"]),
            Paragraph(f"{metrics['manual_share']:.1f}%", styles["FMCell"]),
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[6.1 * cm, 6.1 * cm, 6.1 * cm, 6.1 * cm],
    )
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAF0FB")),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#F8FAFD")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDE5F0")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DDE5F0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Executive interpretation", styles["FMHeading"]))
    longest_wait = df.loc[df["avg_wait_hours"].idxmax()]
    highest_rework = df.loc[df["rework_rate_pct"].idxmax()]
    story.append(Paragraph(
        f"<b>Largest waiting-time signal:</b> "
        f"{html.escape(str(longest_wait['process_step']))} "
        f"({float(longest_wait['avg_wait_hours']):.1f} hours). "
        f"<b>Highest rework signal:</b> "
        f"{html.escape(str(highest_rework['process_step']))} "
        f"({float(highest_rework['rework_rate_pct']):.1f}%).",
        styles["FMBody"],
    ))
    story.append(Paragraph(
        "Interpretation note: these metrics summarize the supplied process-step "
        "averages. They are not a measured end-to-end customer journey unless "
        "the source data represents comparable cases and time periods.",
        styles["FMBody"],
    ))

    if scenario:
        story.append(Paragraph("What-if scenario", styles["FMHeading"]))
        story.append(Paragraph(
            f"Assumed waiting-time reduction: {scenario['wait_reduction']}%; "
            f"work-time reduction: {scenario['work_reduction']}%; "
            f"rework-rate reduction: {scenario['rework_reduction']}%. "
            f"Estimated modeled time after scenario: "
            f"{scenario['future_time']:.1f} hours, compared with "
            f"{scenario['baseline_time']:.1f} hours in the baseline. "
            f"Estimated time difference: {scenario['hours_saved']:.1f} hours.",
            styles["FMBody"],
        ))
        story.append(Paragraph(
            "These figures are scenario estimates based on user-selected "
            "assumptions, not guaranteed savings or measured outcomes.",
            styles["FMBody"],
        ))

    story.append(Paragraph("Process-step performance", styles["FMHeading"]))

    process_headers = [
        "Process step", "Activity", "Work (hrs)", "Wait (hrs)",
        "Cost (INR)", "Rework (%)",
    ]
    process_data = [[Paragraph(x, styles["FMCellBold"]) for x in process_headers]]

    for _, row in df.iterrows():
        process_data.append([
            Paragraph(html.escape(str(row["process_step"])), styles["FMCell"]),
            Paragraph(html.escape(str(row["activity_type"])), styles["FMCell"]),
            Paragraph(f"{float(row['avg_work_hours']):.1f}", styles["FMCell"]),
            Paragraph(f"{float(row['avg_wait_hours']):.1f}", styles["FMCell"]),
            Paragraph(f"{float(row['avg_cost_inr']):,.0f}", styles["FMCell"]),
            Paragraph(f"{float(row['rework_rate_pct']):.1f}", styles["FMCell"]),
        ])

    process_table = Table(
        process_data,
        colWidths=[7.3 * cm, 3.1 * cm, 2.4 * cm, 2.4 * cm, 3.1 * cm, 2.4 * cm],
        repeatRows=1,
        hAlign="LEFT",
    )
    process_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17233D")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white, colors.HexColor("#F5F8FC")
        ]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DDE5F0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(process_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Prioritized recommendations", styles["FMHeading"]))

    rec_headers = [
        "Process step", "Priority", "Score", "Key signals", "Recommended action"
    ]
    rec_data = [[Paragraph(x, styles["FMCellBold"]) for x in rec_headers]]

    for _, row in recs.iterrows():
        rec_data.append([
            Paragraph(html.escape(str(row["process_step"])), styles["FMCell"]),
            Paragraph(html.escape(str(row["priority"])), styles["FMCell"]),
            Paragraph(f"{float(row['opportunity_score']):.1f}/100", styles["FMCell"]),
            Paragraph(html.escape(str(row["key_signals"])), styles["FMCell"]),
            Paragraph(html.escape(str(row["recommended_action"])), styles["FMCell"]),
        ])

    rec_table = Table(
        rec_data,
        colWidths=[4.2 * cm, 2.0 * cm, 2.0 * cm, 7.2 * cm, 8.5 * cm],
        repeatRows=1,
        hAlign="LEFT",
    )
    rec_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17233D")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white, colors.HexColor("#F5F8FC")
        ]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DDE5F0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Methodology &amp; limitations", styles["FMHeading"]))
    story.append(Paragraph(
        "Opportunity scores are transparent heuristic rankings derived from "
        "normalized waiting time, rework, work effort, cost, and activity type. "
        "They are not machine-learning predictions. Recommendations are "
        "decision-support suggestions and should be validated with process "
        "owners before implementation. Costs are the supplied per-step "
        "values; totals should only be interpreted as comparable modeled "
        "totals if the input data uses consistent units and scope.",
        styles["FMBody"],
    ))

    def add_footer(canvas, document):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#DDE5F0"))
        canvas.line(1.25 * cm, 0.95 * cm, page_size[0] - 1.25 * cm, 0.95 * cm)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#78869B"))
        canvas.drawString(1.25 * cm, 0.55 * cm, "FLOWMIND AI | Process Intelligence")
        canvas.drawRightString(
            page_size[0] - 1.25 * cm,
            0.55 * cm,
            f"Version {APP_VERSION} | Page {document.page}",
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    return buffer.getvalue()


# ============================================================
# SIDEBAR: BRAND, NAVIGATION, AND DATA UPLOAD
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">◈</div>
            <div class="brand-title">FLOWMIND AI</div>
            <div class="brand-subtitle">Process Intelligence</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**WORKSPACE**")
    page = st.radio(
        "Navigate",
        NAV_ITEMS,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**DATA SOURCE**")
    uploaded_file = st.file_uploader(
        "Upload process data",
        type=["csv", "xlsx"],
        help="CSV or Excel file with the six required process columns.",
    )
    st.caption(
        "Required: process_step, avg_work_hours, avg_wait_hours, "
        "avg_cost_inr, rework_rate_pct, activity_type"
    )

    st.markdown("---")
    st.markdown("**QUICK GUIDE**")
    st.caption("01  Discover process friction")
    st.caption("02  Simulate possible improvements")
    st.caption("03  Prioritize actions")
    st.caption("04  Export your findings")

    st.markdown("---")
    st.caption(f"FLOWMIND AI • Version {APP_VERSION}")


# ============================================================
# LOAD DATA AND TRACK SOURCE
# ============================================================

is_demo = uploaded_file is None
data_error = None

if is_demo:
    df = sample_data()
else:
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            raw_df = pd.read_csv(uploaded_file)
        else:
            raw_df = pd.read_excel(uploaded_file)

        df, validation_errors = validate_data(raw_df)

        if validation_errors:
            data_error = " ".join(validation_errors)
            df = sample_data()
            is_demo = True
    except Exception as exc:
        data_error = (
            "Could not read the uploaded file. Check the file format and "
            "make sure the required columns are present."
        )
        df = sample_data()
        is_demo = True

df = df.copy()
metrics = calculate_metrics(df)
recommendations = build_recommendations(df)

if data_error:
    st.error(data_error)
    st.warning(
        "The app is displaying the demonstration dataset until the uploaded "
        "file is corrected."
    )

source_badge = (
    '<span class="demo-pill">DEMO DATASET</span>'
    if is_demo
    else '<span class="live-pill">UPLOADED DATA</span>'
)


# ============================================================
# SHARED HEADER
# ============================================================

st.markdown(
    f"""
    <div style="display:flex; justify-content:space-between; align-items:center;
                gap:12px; flex-wrap:wrap; margin-bottom:9px;">
        <div class="eyebrow">OPERATIONAL INTELLIGENCE PLATFORM</div>
        <div>{source_badge}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if is_demo:
    st.caption(
        "Illustrative sample data is active. Upload a CSV or Excel file to "
        "analyze your own process."
    )


# ============================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">See the friction. Find the opportunity.</div>
            <div class="hero-title">Turn process complexity into clarity.</div>
            <div class="hero-copy">
                Discover where time disappears, where rework accumulates, and
                which operational improvements deserve attention first.
                Explore the evidence before making the decision.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        (
            c1,
            "TOTAL MODELED TIME",
            f"{metrics['total_time']:,.1f} hrs",
            f"{metrics['total_wait']:,.1f} hours waiting",
        ),
        (
            c2,
            "MODELED STEP COST",
            format_inr(metrics["total_cost"]),
            "Sum of supplied per-step cost values",
        ),
        (
            c3,
            "AVERAGE REWORK RATE",
            f"{metrics['avg_rework']:.1f}%",
            "Simple average across process steps",
        ),
        (
            c4,
            "MANUAL ACTIVITY SHARE",
            f"{metrics['manual_share']:.0f}%",
            "Share of steps marked Manual",
        ),
    ]

    for col, label, value, note in cards:
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        st.markdown(
            '<div class="section-heading">Where does time go?</div>'
            '<div class="section-copy">Compare active work with waiting '
            'at every process step.</div>',
            unsafe_allow_html=True,
        )

        time_df = df[[
            "process_step", "avg_work_hours", "avg_wait_hours"
        ]].melt(
            id_vars="process_step",
            var_name="time_type",
            value_name="hours",
        )
        time_df["time_type"] = time_df["time_type"].map({
            "avg_work_hours": "Work hours",
            "avg_wait_hours": "Waiting hours",
        })

        fig = px.bar(
            time_df,
            x="process_step",
            y="hours",
            color="time_type",
            barmode="group",
            color_discrete_map={
                "Work hours": COLORS["blue"],
                "Waiting hours": COLORS["cyan"],
            },
            labels={
                "process_step": "Process step",
                "hours": "Hours",
                "time_type": "Measure",
            },
        )
        fig.update_xaxes(tickangle=-25)
        st.plotly_chart(make_chart_layout(fig, 380), use_container_width=True)

    with right:
        st.markdown(
            '<div class="section-heading">Rework pressure</div>'
            '<div class="section-copy">Steps with higher rework may need '
            'stronger validation or clearer standards.</div>',
            unsafe_allow_html=True,
        )

        rework_df = df.sort_values("rework_rate_pct", ascending=True)
        fig2 = px.bar(
            rework_df,
            x="rework_rate_pct",
            y="process_step",
            orientation="h",
            color="rework_rate_pct",
            color_continuous_scale=["#9DE8DB", "#4776F5", "#E66B78"],
            labels={
                "rework_rate_pct": "Rework rate (%)",
                "process_step": "",
            },
        )
        fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(make_chart_layout(fig2, 380), use_container_width=True)

    st.markdown(
        '<div class="section-heading">The business signals</div>'
        '<div class="section-copy">Evidence-based observations calculated '
        'from the currently loaded data.</div>',
        unsafe_allow_html=True,
    )

    longest_wait = df.loc[df["avg_wait_hours"].idxmax()]
    highest_rework = df.loc[df["rework_rate_pct"].idxmax()]
    highest_cost = df.loc[df["avg_cost_inr"].idxmax()]

    signal_cols = st.columns(3)
    signals = [
        (
            signal_cols[0],
            "Longest waiting time",
            f"{longest_wait['process_step']}: "
            f"{longest_wait['avg_wait_hours']:.1f} hours.",
            "Review queues, handoffs, ownership, and service-level targets.",
            COLORS["blue"],
        ),
        (
            signal_cols[1],
            "Highest rework rate",
            f"{highest_rework['process_step']}: "
            f"{highest_rework['rework_rate_pct']:.1f}%.",
            "Investigate recurring errors and opportunities for earlier validation.",
            COLORS["red"],
        ),
        (
            signal_cols[2],
            "Highest modeled step cost",
            f"{highest_cost['process_step']}: "
            f"{format_inr(highest_cost['avg_cost_inr'])}.",
            "Check the cost drivers and confirm whether cost units are comparable.",
            COLORS["orange"],
        ),
    ]

    for col, title, finding, action, accent in signals:
        with col:
            st.markdown(
                f"""
                <div class="insight-card" style="border-left-color:{accent}">
                    <div class="insight-title">{title}</div>
                    <div class="insight-copy"><b>{html.escape(finding)}</b><br>
                    {html.escape(action)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-heading">Priority radar</div>'
        '<div class="section-copy">A transparent heuristic score ranks '
        'potential improvement opportunities; it is not a trained AI model.</div>',
        unsafe_allow_html=True,
    )

    radar_cols = st.columns(3)
    for col, priority in zip(radar_cols, ["High", "Medium", "Low"]):
        count = int((recommendations["priority"] == priority).sum())
        with col:
            st.markdown(
                f"""
                <div class="metric-card" style="min-height:90px">
                    <div class="metric-label">{priority.upper()} PRIORITY</div>
                    <div class="metric-value">{count}</div>
                    <div class="metric-note">process step(s)</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    st.download_button(
        "Download overview data (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="flowmind_process_data.csv",
        mime="text/csv",
    )


# ============================================================
# PAGE 2: WHAT-IF ANALYSIS
# ============================================================

elif page == "What-If Analysis":
    st.markdown("# What-If Scenario Lab")
    st.markdown(
        '<div class="page-subtitle">Model a possible future state by adjusting '
        'improvement assumptions. These are estimates, not guaranteed results.</div>',
        unsafe_allow_html=True,
    )

    base = calculate_metrics(df)

    left, right = st.columns([0.75, 1.25], gap="large")

    with left:
        st.markdown("### Adjust improvement assumptions")
        wait_reduction = st.slider(
            "Waiting-time reduction (%)", 0, 80, 25, 5
        )
        work_reduction = st.slider(
            "Work-time reduction (%)", 0, 50, 10, 5
        )
        rework_reduction = st.slider(
            "Rework-rate reduction (%)", 0, 70, 20, 5
        )
        st.caption(
            "Adjust the sliders to test different assumptions. The app does "
            "not claim that the reductions will automatically occur."
        )

    future_wait = base["total_wait"] * (1 - wait_reduction / 100)
    future_work = base["total_work"] * (1 - work_reduction / 100)
    future_time = future_wait + future_work
    hours_saved = base["total_time"] - future_time
    time_reduction = (
        hours_saved / base["total_time"] * 100
        if base["total_time"] > 0 else 0
    )
    future_rework = base["avg_rework"] * (1 - rework_reduction / 100)

    scenario = {
        "wait_reduction": wait_reduction,
        "work_reduction": work_reduction,
        "rework_reduction": rework_reduction,
        "baseline_time": base["total_time"],
        "future_time": future_time,
        "hours_saved": hours_saved,
        "future_rework": future_rework,
        "time_reduction": time_reduction,
    }

    with right:
        st.markdown("### Your modeled future state")
        m1, m2 = st.columns(2)

        with m1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">MODELED HOURS DIFFERENCE</div>
                    <div class="metric-value">{hours_saved:,.1f}</div>
                    <div class="metric-note">Difference between baseline and scenario</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with m2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">MODELED TIME REDUCTION</div>
                    <div class="metric-value">{time_reduction:.1f}%</div>
                    <div class="metric-note">Based on your selected assumptions</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")
        comparison = pd.DataFrame({
            "Scenario": ["Current baseline", "Modeled future state"],
            "Work hours": [base["total_work"], future_work],
            "Waiting hours": [base["total_wait"], future_wait],
        })

        chart_data = comparison.melt(
            id_vars="Scenario",
            var_name="Measure",
            value_name="Hours",
        )

        scenario_fig = px.bar(
            chart_data,
            x="Scenario",
            y="Hours",
            color="Measure",
            barmode="group",
            color_discrete_map={
                "Work hours": COLORS["blue"],
                "Waiting hours": COLORS["cyan"],
            },
            text_auto=".1f",
        )
        st.plotly_chart(
            make_chart_layout(scenario_fig, 330),
            use_container_width=True,
        )

    st.markdown("### Assumption summary")
    scenario_table = pd.DataFrame([
        {
            "Metric": "Total modeled time",
            "Current baseline": round(base["total_time"], 2),
            "Modeled future state": round(future_time, 2),
            "Unit": "hours",
        },
        {
            "Metric": "Waiting time",
            "Current baseline": round(base["total_wait"], 2),
            "Modeled future state": round(future_wait, 2),
            "Unit": "hours",
        },
        {
            "Metric": "Work time",
            "Current baseline": round(base["total_work"], 2),
            "Modeled future state": round(future_work, 2),
            "Unit": "hours",
        },
        {
            "Metric": "Average rework rate",
            "Current baseline": round(base["avg_rework"], 2),
            "Modeled future state": round(future_rework, 2),
            "Unit": "%",
        },
    ])
    st.dataframe(scenario_table, use_container_width=True, hide_index=True)

    st.info(
        "Interpretation: this simulator applies your chosen percentage "
        "reductions to the current totals. It does not infer causality, "
        "account for dependencies between steps, or forecast actual outcomes. "
        "Validate assumptions with process owners before making commitments."
    )

    scenario_export = pd.DataFrame([{
        **scenario,
        "baseline_cost_inr": base["total_cost"],
        "cost_savings_estimate": None,
        "cost_savings_note": (
            "Not estimated: no cost-reduction assumption was provided."
        ),
    }])

    st.download_button(
        "Download scenario assumptions (CSV)",
        data=scenario_export.to_csv(index=False).encode("utf-8"),
        file_name="flowmind_what_if_scenario.csv",
        mime="text/csv",
    )


# ============================================================
# PAGE 3: RECOMMENDATIONS
# ============================================================

elif page == "Recommendations":
    st.markdown("# Improvement Opportunity Radar")
    st.markdown(
        '<div class="page-subtitle">Prioritize actions using a transparent '
        'heuristic that combines waiting time, rework, work effort, cost, '
        'and activity type.</div>',
        unsafe_allow_html=True,
    )

    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric(
            "High priority",
            int((recommendations["priority"] == "High").sum()),
        )
    with r2:
        st.metric(
            "Medium priority",
            int((recommendations["priority"] == "Medium").sum()),
        )
    with r3:
        st.metric(
            "Low priority",
            int((recommendations["priority"] == "Low").sum()),
        )

    st.caption(
        "Opportunity score ranges from 0 to 100. It is a rule-based ranking "
        "for decision support, not a probability of success or a trained "
        "machine-learning prediction."
    )

    priority_filter = st.multiselect(
        "Filter by priority",
        options=["High", "Medium", "Low"],
        default=["High", "Medium", "Low"],
    )

    filtered_recs = recommendations[
        recommendations["priority"].isin(priority_filter)
    ].copy()

    display_recs = filtered_recs.rename(columns={
        "process_step": "Process step",
        "priority": "Priority",
        "opportunity_score": "Opportunity score",
        "activity_type": "Activity type",
        "avg_wait_hours": "Wait (hours)",
        "rework_rate_pct": "Rework (%)",
        "avg_cost_inr": "Cost (INR)",
        "key_signals": "Key signals",
        "recommended_action": "Recommended action",
    })

    st.dataframe(
        display_recs,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Opportunity score": st.column_config.ProgressColumn(
                "Opportunity score",
                min_value=0,
                max_value=100,
                format="%.1f",
            ),
            "Cost (INR)": st.column_config.NumberColumn(
                "Cost (INR)",
                format="₹%.0f",
            ),
        },
    )

    st.download_button(
        "Download recommendations (CSV)",
        data=filtered_recs.to_csv(index=False).encode("utf-8"),
        file_name="flowmind_recommendations.csv",
        mime="text/csv",
    )

    st.markdown("### Recommended next actions")

    if filtered_recs.empty:
        st.info("No process steps match the selected priority filters.")
    else:
        for _, row in filtered_recs.iterrows():
            with st.expander(
                f"{row['priority']} | {row['process_step']} | "
                f"Score {row['opportunity_score']:.1f}/100"
            ):
                st.write("**Observed signals**")
                st.write(row["key_signals"])
                st.write("**Suggested actions**")
                for action in str(row["recommended_action"]).split("; "):
                    st.markdown(f"- {action}")
                st.caption(
                    "Confirm the root cause and implementation effort with "
                    "the process owner before committing resources."
                )


# ============================================================
# PAGE 4: MANAGEMENT REPORT
# ============================================================

elif page == "Management Report":
    st.markdown("# Executive Management Report")
    st.markdown(
        '<div class="page-subtitle">Create a shareable report with key metrics, '
        'process-step data, prioritized recommendations, and transparent '
        'methodology notes.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Process steps", len(df))
    with c2:
        st.metric("Total modeled time", f"{metrics['total_time']:.1f} hrs")
    with c3:
        st.metric("Recommendations", len(recommendations))

    st.markdown("### Report contents")
    st.markdown(
        "- Executive summary and key process signals\n"
        "- Process-step performance table\n"
        "- Prioritized improvement recommendations\n"
        "- Methodology and limitations\n"
        "- Optional What-If scenario assumptions"
    )

    include_scenario = st.checkbox(
        "Include current What-If scenario assumptions in the PDF",
        value=False,
    )

    scenario_for_pdf = None
    if include_scenario:
        st.caption(
            "Set assumptions on the What-If Analysis page first. If you have "
            "not visited it during this session, the default assumptions "
            "below are used."
        )
        wait_r = st.number_input(
            "Assumed waiting-time reduction (%)",
            min_value=0,
            max_value=80,
            value=25,
            step=5,
        )
        work_r = st.number_input(
            "Assumed work-time reduction (%)",
            min_value=0,
            max_value=50,
            value=10,
            step=5,
        )
        rework_r = st.number_input(
            "Assumed rework-rate reduction (%)",
            min_value=0,
            max_value=70,
            value=20,
            step=5,
        )

        future_time = (
            metrics["total_wait"] * (1 - wait_r / 100)
            + metrics["total_work"] * (1 - work_r / 100)
        )

        scenario_for_pdf = {
            "wait_reduction": wait_r,
            "work_reduction": work_r,
            "rework_reduction": rework_r,
            "baseline_time": metrics["total_time"],
            "future_time": future_time,
            "hours_saved": metrics["total_time"] - future_time,
        }

    if st.button("Generate PDF report", type="primary"):
        try:
            pdf_bytes = generate_pdf(
                df,
                recommendations,
                metrics,
                scenario_for_pdf,
            )
            st.download_button(
                "Download FLOWMIND AI Management Report",
                data=pdf_bytes,
                file_name="flowmind_ai_management_report.pdf",
                mime="application/pdf",
            )
            st.success("Your PDF report is ready to download.")
        except Exception as exc:
            st.error(
                "The PDF could not be generated. Check that ReportLab is "
                "installed in the project's virtual environment."
            )
            st.exception(exc)


# ============================================================
# PAGE 5: DETAILED PROCESS DATA
# ============================================================

elif page == "Detailed Process Data":
    st.markdown("# Process Data Explorer")
    st.markdown(
        '<div class="page-subtitle">Inspect, search, filter, and export the '
        'records powering your process analysis.</div>',
        unsafe_allow_html=True,
    )

    search_text = st.text_input(
        "Search process step",
        placeholder="Type a process name...",
    )

    activity_options = sorted(df["activity_type"].dropna().unique().tolist())
    selected_activities = st.multiselect(
        "Filter by activity type",
        options=activity_options,
        default=activity_options,
    )

    filtered_df = df.copy()

    if search_text.strip():
        filtered_df = filtered_df[
            filtered_df["process_step"].str.contains(
                search_text.strip(),
                case=False,
                na=False,
            )
        ]

    filtered_df = filtered_df[
        filtered_df["activity_type"].isin(selected_activities)
    ]

    st.caption(
        f"Showing {len(filtered_df)} of {len(df)} process steps."
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "avg_work_hours": st.column_config.NumberColumn(
                "avg_work_hours", format="%.2f"
            ),
            "avg_wait_hours": st.column_config.NumberColumn(
                "avg_wait_hours", format="%.2f"
            ),
            "avg_cost_inr": st.column_config.NumberColumn(
                "avg_cost_inr", format="₹%.0f"
            ),
            "rework_rate_pct": st.column_config.NumberColumn(
                "rework_rate_pct", format="%.1f%%"
            ),
        },
    )

    st.download_button(
        "Export filtered data (CSV)",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="flowmind_filtered_process_data.csv",
        mime="text/csv",
    )

    st.markdown("### Data quality checklist")
    checks = [
        ("Required columns", all(c in df.columns for c in REQUIRED_COLUMNS)),
        ("No missing process-step names", not df["process_step"].isna().any()),
        (
            "Non-negative work, wait, and cost",
            (df[["avg_work_hours", "avg_wait_hours", "avg_cost_inr"]] >= 0)
            .all().all(),
        ),
        (
            "Rework rate between 0% and 100%",
            df["rework_rate_pct"].between(0, 100).all(),
        ),
    ]

    for label, passed in checks:
        if passed:
            st.success(f"Passed: {label}")
        else:
            st.error(f"Check required: {label}")


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    f"""
    <div class="footer">
        FLOWMIND AI &nbsp;•&nbsp; PROCESS INTELLIGENCE & OPTIMIZATION
        <span style="float:right">VERSION {APP_VERSION}</span><br>
        Explainable analytics for better operational decisions.
    </div>
    """,
    unsafe_allow_html=True,
)
