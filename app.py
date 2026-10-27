
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
    page_icon="assets/flowmind-icon.svg",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_VERSION = "4.4"

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
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
        font-family: 'Space Grotesk', sans-serif !important;
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
        padding: 12px 3px 25px 3px;
        border-bottom: 1px solid rgba(255,255,255,.10);
        margin-bottom: 20px;
    }
    .brand-lockup { display:flex; align-items:center; gap:12px; margin-bottom:15px; }
    .brand-symbol { width:58px; height:58px; flex:0 0 58px; display:block; filter: drop-shadow(0 3px 8px rgba(39,200,232,.12)); }
    .brand-lockup { display:flex; align-items:center; gap:12px; margin-bottom:13px; }
    .brand-tagline { color:#C2D5F1; font-size:9px; letter-spacing:1.75px; text-transform:uppercase; margin-top:6px; font-weight:700; }
    .brand-byline { color:#91A6C7; font-size:10px; letter-spacing:.1px; line-height:1.5; margin-top:10px; }
    .workspace-intro { padding: 4px 0 16px; }
    .workspace-eyebrow { color:#2877A8; font-size:10px; font-weight:800; letter-spacing:2px; text-transform:uppercase; margin-bottom:10px; }
    .workspace-headline { font-family:'Sora','Space Grotesk',sans-serif; color:#0B1530; font-size:clamp(27px,3vw,42px); font-weight:700; letter-spacing:-1.65px; line-height:1.12; margin:0 0 12px 0; max-width:850px; }
    .workspace-headline .accent { color:#159DBB; }
    .workspace-copy { font-family:'Inter',sans-serif; color:#64748B; font-size:14px; line-height:1.75; max-width:760px; margin-bottom:2px; }
    .upload-panel-title { font-family:'Sora','Space Grotesk',sans-serif; color:#0B1530; font-size:18px; font-weight:650; letter-spacing:-.4px; margin:0 0 5px 0; }
    @media (max-width: 640px) { .workspace-headline { font-size:clamp(27px,7.5vw,34px); letter-spacing:-1px; line-height:1.14; } .workspace-copy {font-size:13px;} .brand-symbol {width:48px;height:48px;flex-basis:48px;} }
    .brand-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 21px;
        font-weight: 700;
        letter-spacing: -.7px;
        color: #FFFFFF;
        line-height: 1.1;
    }
    .brand-title span { color:#43D7F2; }
    .brand-subtitle {
        color: #A9B9D8;
        font-size: 9px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 7px;
        font-weight:700;
    }
    .brand-byline {
        color: #9EB7E8;
        font-size: 11px;
        letter-spacing: .5px;
        margin-top: 5px;
    }
    .hero-actions-note {
        color: #66758C;
        font-size: 12px;
        padding-top: 8px;
    }

    .brand-title {
        font-family: 'Space Grotesk', sans-serif;
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
        font-family: 'Space Grotesk', sans-serif;
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
        font-family: 'Space Grotesk', sans-serif;
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
        font-family: 'Space Grotesk', sans-serif;
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

    /* Responsive dashboard improvements */
    @media (max-width: 768px) {
        .hero { padding: 22px 18px; border-radius: 15px; margin-bottom: 16px; }
        .hero-title { font-size: 23px; line-height: 1.25; }
        .hero-copy { font-size: 13px; }
        .metric-card { padding: 14px; min-height: auto; border-radius: 13px; }
        .metric-label { font-size: 10px; letter-spacing: .6px; }
        .metric-value { font-size: 22px; overflow-wrap: anywhere; }
        .metric-note { font-size: 11px; }
        .section-heading { font-size: 16px; }
        .page-subtitle { font-size: 13px; margin-bottom: 16px; }
        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; gap: .65rem !important; }
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            min-width: min(100%, 260px) !important;
            flex: 1 1 100% !important;
            width: 100% !important;
        }
        [data-testid="stPlotlyChart"] { padding: 2px; }
        [data-testid="stDataFrame"] { overflow-x: auto; }
        div[data-testid="stButton"] button,
        div[data-testid="stDownloadButton"] button,
        div[data-testid="stFileUploader"] button {
            width: 100%;
            min-height: 44px;
            white-space: normal;
        }
        [data-testid="stFileUploaderDropzone"] { padding: 12px !important; }
        .footer { line-height: 1.8; }
    }
    @media (max-width: 480px) {
        .hero-title { font-size: 21px; }
        .metric-value { font-size: 20px; }
        h1 { font-size: 1.65rem !important; }
        h2 { font-size: 1.35rem !important; }
        h3 { font-size: 1.12rem !important; }
    }

    /* FLOWMIND 4.2 — editorial typography and premium interaction layer */
    :root {
        --fm-ink: #101A33;
        --fm-navy: #0B1530;
        --fm-cyan: #22C8E5;
        --fm-slate: #65738B;
        --fm-line: #DCE5F0;
        --fm-paper: #F7F9FC;
    }
    .stApp { background: var(--fm-paper); }
    [data-testid="stMain"] > div { padding-top: 1.35rem; }
    [data-testid="stSidebar"] { background: linear-gradient(160deg,#09142C 0%,#101F3C 65%,#102B46 100%); }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#B9C8E2; }
    [data-testid="stSidebar"] hr { border-color:rgba(183,207,243,.15); }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color:#91A5C8; }
    h1, h2, h3, h4 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.045em !important; }
    h1 { font-weight:700 !important; color:var(--fm-ink) !important; }
    h2 { font-weight:650 !important; color:var(--fm-ink) !important; }
    h3 { font-weight:650 !important; color:#1A2B4A !important; }
    p, label, input, textarea, button, [data-testid="stMarkdownContainer"] { font-family:'Inter',sans-serif; }
    .eyebrow { color:#2874D9; letter-spacing:2.1px; font-size:10px; font-weight:800; }
    .hero {
        position:relative; overflow:hidden;
        background: radial-gradient(ellipse at 95% 8%,rgba(34,200,229,.20),transparent 32%),
                    linear-gradient(118deg,#0A1530 0%,#13294C 62%,#164764 100%);
        padding:clamp(25px,4vw,42px); border:1px solid rgba(133,199,237,.22);
        border-radius:22px; box-shadow:0 18px 45px rgba(10,25,52,.13);
    }
    .hero:after { content:""; position:absolute; width:210px; height:210px; right:-80px; bottom:-120px; border:1px solid rgba(74,218,242,.25); border-radius:50%; box-shadow:0 0 0 22px rgba(74,218,242,.035),0 0 0 44px rgba(74,218,242,.025); pointer-events:none; }
    .hero-kicker { color:#7BE7F2; letter-spacing:2.4px; font-size:10px; }
    .hero-title { font-family:'Space Grotesk',sans-serif !important; font-size:clamp(27px,3.2vw,43px); line-height:1.08; letter-spacing:-1.8px; max-width:780px; margin-bottom:13px; }
    .hero-copy { color:#D5E2F5; font-size:14px; line-height:1.8; max-width:700px; }
    .metric-card { border:1px solid #E1E8F2; border-radius:17px; box-shadow:0 5px 18px rgba(17,35,67,.035); transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease; }
    .metric-card:hover { transform:translateY(-2px); border-color:#B6D8EA; box-shadow:0 12px 28px rgba(17,35,67,.075); }
    .metric-label { font-size:10px; letter-spacing:1.15px; color:#65738B; }
    .metric-value { font-variant-numeric:tabular-nums; letter-spacing:-1px; }
    .section-heading { font-family:'Space Grotesk',sans-serif; letter-spacing:-.5px; }
    .insight-card { border:1px solid #E1E8F2; border-left:3px solid #22C8E5; box-shadow:0 4px 16px rgba(17,35,67,.025); }
    div[data-testid="stDownloadButton"] button, div[data-testid="stButton"] button, [data-testid="stFormSubmitButton"] button {
        border-radius:10px; font-weight:650; letter-spacing:-.15px; min-height:43px;
        transition:transform .16s ease,box-shadow .16s ease,border-color .16s ease;
    }
    div[data-testid="stButton"] button[kind="primary"], [data-testid="stFormSubmitButton"] button[kind="primary"] { background:linear-gradient(115deg,#1767D2,#168BB8); border:0; box-shadow:0 6px 16px rgba(23,103,210,.18); }
    div[data-testid="stButton"] button:hover, div[data-testid="stDownloadButton"] button:hover { transform:translateY(-1px); border-color:#7ABFD9; box-shadow:0 7px 18px rgba(16,48,83,.09); }
    [data-testid="stSelectbox"] > div > div, [data-testid="stTextInput"] input { border-radius:10px; }
    [data-testid="stFileUploaderDropzone"] { border:1px dashed #A7BDD5 !important; border-radius:14px !important; background:linear-gradient(135deg,#F8FBFF,#F1F7FC) !important; }
    [data-testid="stExpander"] { border:1px solid #DFE7F1; border-radius:12px; background:rgba(255,255,255,.68); }
    [data-testid="stPlotlyChart"] { box-shadow:0 5px 18px rgba(17,35,67,.035); }
    .footer { font-size:10px; letter-spacing:.55px; }
    @media (max-width:768px) {
        [data-testid="stMain"] > div { padding-top:.7rem; }
        .hero { border-radius:16px; }
        .hero-title { letter-spacing:-1px; }
        .brand { padding-bottom:17px; }
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


def create_sample_template() -> bytes:
    """Build a real Excel template using the application's required schema."""
    template_df = sample_data()
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        template_df.to_excel(writer, index=False, sheet_name="Process Data")
        instructions = pd.DataFrame({
            "Column": REQUIRED_COLUMNS,
            "What to enter": [
                "Name of the process step",
                "Average active work time, in hours",
                "Average waiting time, in hours",
                "Average cost for this step, in INR",
                "Rework percentage from 0 to 100",
                "Manual, Digital, or Automated (or another clear activity label)",
            ],
        })
        instructions.to_excel(writer, index=False, sheet_name="Instructions")
        workbook = writer.book
        ws = workbook["Process Data"]
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        for column_cells in ws.columns:
            letter = column_cells[0].column_letter
            ws.column_dimensions[letter].width = min(
                max(max(len(str(cell.value or "")) for cell in column_cells) + 3, 16),
                32,
            )
        instruction_ws = workbook["Instructions"]
        instruction_ws.freeze_panes = "A2"
        instruction_ws.column_dimensions["A"].width = 25
        instruction_ws.column_dimensions["B"].width = 68
    buffer.seek(0)
    return buffer.getvalue()


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

# Navigation is driven by explicit button callbacks rather than widget selection state.
def set_active_workspace_page(page_name: str) -> None:
    st.session_state["active_workspace_page"] = page_name

if "active_workspace_page" not in st.session_state:
    st.session_state["active_workspace_page"] = NAV_ITEMS[0]

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
          <div class="brand-lockup">
            <svg class="brand-symbol" viewBox="0 0 100 100" role="img" aria-label="FlowMind AI Intelligence Flow symbol">
              <defs>
                <linearGradient id="flowmindStroke" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stop-color="#FFFFFF"/>
                  <stop offset="100%" stop-color="#27C8E8"/>
                </linearGradient>
              </defs>
              <path d="M16 30 C28 14 42 17 49 32 C56 47 65 49 82 31" fill="none" stroke="url(#flowmindStroke)" stroke-width="5.2" stroke-linecap="round"/>
              <path d="M13 51 C27 37 38 39 49 52 C60 65 72 66 87 49" fill="none" stroke="#27C8E8" stroke-width="4.2" stroke-linecap="round"/>
              <path d="M19 72 C31 60 41 62 50 72 C59 82 70 81 81 69" fill="none" stroke="#FFFFFF" stroke-opacity=".88" stroke-width="3.5" stroke-linecap="round"/>
              <path d="M49 32 C42 42 43 58 50 72" fill="none" stroke="#7BE7F5" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="2 5"/>
              <circle cx="16" cy="30" r="4.2" fill="#27C8E8"/><circle cx="82" cy="31" r="4.2" fill="#FFFFFF"/>
              <circle cx="13" cy="51" r="3.8" fill="#FFFFFF"/><circle cx="87" cy="49" r="4.2" fill="#27C8E8"/>
              <circle cx="19" cy="72" r="3.5" fill="#27C8E8"/><circle cx="81" cy="69" r="3.5" fill="#FFFFFF"/>
              <circle cx="49" cy="52" r="4.6" fill="#0B1530" stroke="#27C8E8" stroke-width="2.6"/>
            </svg>
            <div>
              <div class="brand-title">FLOWMIND <span>AI</span></div>
              <div class="brand-tagline">INTELLIGENCE IN FLOW</div>
            </div>
          </div>
          <div class="brand-byline">An intelligence platform by <strong>Albert Davis</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**YOUR WORKSPACE**")
    st.caption("Choose a section to open it. The active section is highlighted.")
    for nav_item in NAV_ITEMS:
        st.button(
            nav_item,
            key=f"workspace_nav_{nav_item.lower().replace(' ', '_').replace('-', '_')}",
            type="primary" if st.session_state["active_workspace_page"] == nav_item else "secondary",
            on_click=set_active_workspace_page,
            args=(nav_item,),
            use_container_width=True,
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
# MOBILE-FIRST NAVIGATION AND VISIBLE DATA UPLOAD
# ============================================================

page = st.session_state.get("active_workspace_page", NAV_ITEMS[0])
nav_col, upload_status_col = st.columns([1.15, 0.85], gap="medium")
with nav_col:
    st.markdown(
        '<div style="padding:10px 13px;border:1px solid #DCE5F0;border-radius:12px;'
        'background:#FFFFFF;font-size:13px;color:#17233D">'
        '<span style="color:#64748B;font-size:10px;font-weight:800;letter-spacing:1.2px">CURRENT WORKSPACE</span><br>'
        f'<strong>{html.escape(page)}</strong></div>',
        unsafe_allow_html=True,
    )
with upload_status_col:
    st.markdown(
        '<div style="padding-top:8px;font-size:12px;color:#66758C">'
        '<b>Quick tip</b><br>Upload your own process data below, or explore '
        'the interactive demo first.</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <section class="workspace-intro">
      <div class="workspace-eyebrow">PROCESS INTELLIGENCE WORKSPACE</div>
      <h1 class="workspace-headline">Every Process Has a Story.<br><span class="accent">Discover Yours.</span></h1>
      <p class="workspace-copy">Turn your operational data into a clearer view of process performance, friction, and opportunities for improvement.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown('<div class="upload-panel-title">Start with your process data</div>', unsafe_allow_html=True)
    st.caption(
        "Upload a CSV or Excel file to begin exploring your process. Use the sample template if you are getting started."
    )
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx"],
        key="main_process_upload",
        help="Required: process_step, avg_work_hours, avg_wait_hours, "
             "avg_cost_inr, rework_rate_pct, activity_type",
    )
    template_col, template_tip_col = st.columns([1, 1.4], gap="medium")
    with template_col:
        st.download_button(
            "⬇️ Download Sample Template (.xlsx)",
            data=create_sample_template(),
            file_name="flowmind_process_data_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            help="Download a workbook with the required columns and example rows.",
        )
    with template_tip_col:
        st.markdown(
            '<div class="hero-actions-note">Tip: replace the example rows with '
            'your own process steps. Keep the column names unchanged.</div>',
            unsafe_allow_html=True,
        )
    with st.expander("View the required file columns"):
        st.code(
            "process_step, avg_work_hours, avg_wait_hours, avg_cost_inr, "
            "rework_rate_pct, activity_type",
            language="text",
        )
        st.caption(
            "Each row represents one process step. Numeric values must be "
            "non-negative, except rework_rate_pct which must be between 0 and 100."
        )


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
            <div class="hero-kicker">PROCESS INTELLIGENCE PLATFORM</div>
            <div class="hero-title">See the Flow. <span style="color:#58DFF0">Find the Friction.</span></div>
            <div class="hero-copy">
                Turn process data into actionable insights, uncover bottlenecks, and
                discover opportunities for smarter, faster operations. Explore the evidence
                before deciding what to change.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    hero_action_cols = st.columns([1, 1, 2], gap="small")
    with hero_action_cols[0]:
        if st.button("Explore the Dashboard", type="primary", use_container_width=True):
            # This button is already on the Executive Overview page. Avoid
            # changing the selectbox-owned workspace_page state after creation.
            st.session_state["show_how_it_works"] = True
            st.rerun()
    with hero_action_cols[1]:
        if st.button("How it works", use_container_width=True):
            st.session_state["show_how_it_works"] = not st.session_state.get(
                "show_how_it_works", False
            )
    if st.session_state.get("show_how_it_works", False):
        st.info(
            "1. Explore the demo or download the template.  2. Upload your CSV/XLSX.  "
            "3. Review process bottlenecks.  4. Test improvements in What-If Analysis.  "
            "5. Export recommendations and a management report."
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
        st.plotly_chart(make_chart_layout(fig, 380), use_container_width=True, config={"responsive": True, "displaylogo": False})

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
        st.plotly_chart(make_chart_layout(fig2, 380), use_container_width=True, config={"responsive": True, "displaylogo": False})

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
            config={"responsive": True, "displaylogo": False},
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
# FLOWMIND SUPPORT GUIDE — BUILT-IN HELP CHAT
# ============================================================

def support_answer(question: str) -> str:
    """Helpful offline support responses; no API key or user account required."""
    q = question.lower().strip()
    if any(word in q for word in ["upload", "file", "csv", "excel", "xlsx"]):
        return (
            "To analyze your own data, use the process-data upload panel near the top "
            "of the page. Select a `.csv` or `.xlsx` file. It must contain: "
            "`process_step`, `avg_work_hours`, `avg_wait_hours`, `avg_cost_inr`, "
            "`rework_rate_pct`, and `activity_type`. If validation fails, the app "
            "will explain the issue and return to demo data."
        )
    if any(word in q for word in ["what if", "scenario", "simulate", "saving", "savings"]):
        return (
            "Open **What-If Analysis** from the left sidebar workspace navigation. Adjust the "
            "waiting-time, work-time, and rework assumptions to compare a baseline "
            "with a modeled future state. These are scenarios, not guaranteed savings."
        )
    if any(word in q for word in ["recommend", "priority", "score", "opportunity"]):
        return (
            "Open **Recommendations** to review priority levels, opportunity scores, "
            "the signals behind each score, and suggested actions. Scores are "
            "transparent rule-based rankings, not trained machine-learning predictions."
        )
    if any(word in q for word in ["pdf", "report", "download", "export"]):
        return (
            "Use **Management Report** to generate a PDF, or use the CSV download "
            "buttons on the relevant pages to export data and recommendations."
        )
    if any(word in q for word in ["data", "columns", "format", "template", "example"]):
        return (
            "Each row should describe one process step. Required fields are: "
            "`process_step` (name), `avg_work_hours`, `avg_wait_hours`, "
            "`avg_cost_inr`, `rework_rate_pct` (0–100), and `activity_type` "
            "(for example Manual, Digital, or Automated)."
        )
    if any(word in q for word in ["how", "start", "begin", "help", "guide"]):
        return (
            "Start with **Executive Overview** to explore the demo, upload your "
            "own data when ready, try **What-If Analysis**, review **Recommendations**, "
            "then export a **Management Report**. Ask me about uploads, scores, "
            "scenarios, or reports any time."
        )
    return (
        "I can help with uploading CSV/Excel data, required columns, interpreting "
        "opportunity scores, What-If scenarios, recommendations, and PDF/CSV exports. "
        "What would you like to do?"
    )


# Show the welcome dialog once per Streamlit visitor session. Mark it as shown
# BEFORE opening it so page reruns caused by navigation do not reopen the dialog.
# This is session-based; the app currently has no separate account-login system.
if "flowmind_greeting_popup_seen" not in st.session_state:
    st.session_state.flowmind_greeting_popup_seen = True
    _show_flowmind_greeting_on_this_run = True
else:
    _show_flowmind_greeting_on_this_run = False


@st.dialog("Welcome to FLOWMIND AI 👋", width="small")
def flowmind_welcome_dialog() -> None:
    st.markdown(
        "### Hi there — welcome to FLOWMIND AI!\n\n"
        "I’m your FLOWMIND Guide. I can help you explore your process data, "
        "understand bottlenecks, test improvements, and prepare a management report."
    )
    st.info("You can start with the demo data, or upload your own CSV/Excel file near the top of this page.")
    if st.button("Let’s explore", type="primary", use_container_width=True):
        # Force a full-app rerun to close the dialog. The session flag is already
        # True, so subsequent navigation/reruns won't display it again.
        st.rerun()


if _show_flowmind_greeting_on_this_run:
    flowmind_welcome_dialog()

if "flowmind_chat_history" not in st.session_state:
    st.session_state.flowmind_chat_history = [
        ("assistant", "Hi! 👋 Welcome to FLOWMIND AI. I can guide you through uploads, process insights, What-If scenarios, recommendations, and reports. What would you like help with?")
    ]

with st.expander("💬 FLOWMIND Guide · Chat support", expanded=False):
    st.markdown(
        "Ask a question below. This built-in guide works without an external API key."
    )
    for role, message in st.session_state.flowmind_chat_history[-8:]:
        with st.chat_message(role):
            st.markdown(message)
    with st.form("flowmind_support_form", clear_on_submit=True):
        user_question = st.text_input(
            "Your question",
            placeholder="e.g. How do I upload my process data?",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Ask FLOWMIND Guide", use_container_width=True)
    if submitted and user_question.strip():
        st.session_state.flowmind_chat_history.append(("user", user_question.strip()))
        answer = support_answer(user_question)
        st.session_state.flowmind_chat_history.append(("assistant", answer))
        st.rerun()


# ============================================================
# THE EVOLUTION OF WISDOM — PREMIUM CLOSING EXPERIENCE
# ============================================================

st.components.v1.html(
r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: transparent; }
  body { font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #F7F8FC; }
  .wisdom-shell {
    position: relative; isolation: isolate; overflow: hidden; width: 100%; min-height: 690px;
    padding: clamp(30px, 5vw, 68px) clamp(20px, 5vw, 64px);
    border-radius: 24px; color: #F7F8FC;
    background: radial-gradient(ellipse at 12% 15%, rgba(39,200,232,.12), transparent 33%),
                radial-gradient(ellipse at 88% 78%, rgba(212,171,95,.09), transparent 32%),
                linear-gradient(135deg, #080F22 0%, #0B1530 53%, #101D37 100%);
    border: 1px solid rgba(132,177,222,.17);
  }
  .wisdom-shell:before, .wisdom-shell:after { content:""; position:absolute; pointer-events:none; z-index:-1; border-radius:50%; }
  .wisdom-shell:before { width:390px; height:390px; right:-190px; top:-190px; border:1px solid rgba(39,200,232,.12); box-shadow:0 0 0 30px rgba(39,200,232,.018),0 0 0 65px rgba(39,200,232,.014); }
  .wisdom-shell:after { width:280px; height:280px; left:-180px; bottom:-170px; border:1px solid rgba(211,175,111,.15); box-shadow:0 0 0 28px rgba(211,175,111,.025); }
  .wisdom-kicker { color:#8DA4C5; font-size:10px; font-weight:700; letter-spacing:2.8px; text-transform:uppercase; margin-bottom:22px; }
  .wisdom-grid { display:grid; grid-template-columns:minmax(0, .82fr) minmax(0, 1.18fr); gap:clamp(25px, 5vw, 70px); align-items:center; }
  .history { padding:12px 0 28px; opacity:0; transform:translateY(18px); }
  .modern { padding:12px 0 18px; opacity:0; transform:translateY(18px); }
  .in-view .history { animation: rise .9s .08s ease forwards; }
  .in-view .modern { animation: rise .9s .9s ease forwards; }
  .then-label, .now-label { font-size:10px; font-weight:800; letter-spacing:2px; color:#9BAAC2; margin-bottom:18px; }
  .then-label:before { content:""; display:inline-block; width:18px; height:1px; background:#BFA16B; margin:0 9px 3px 0; }
  .now-label:before { content:""; display:inline-block; width:18px; height:1px; background:#27C8E8; margin:0 9px 3px 0; }
  .historic-quote { font-family: Georgia, "Times New Roman", serif; font-weight:400; font-size:clamp(29px, 3.2vw, 45px); letter-spacing:-1.2px; line-height:1.16; color:#E7D9BC; margin:0 0 19px; }
  .historic-by { color:#9FAEC4; font-family:Georgia, "Times New Roman", serif; font-size:14px; letter-spacing:.3px; }
  .bridge { position:relative; display:flex; align-items:center; gap:12px; margin:12px 0 25px; min-height:24px; }
  .bridge-line { height:1px; flex:1; background:linear-gradient(90deg, rgba(191,161,107,.55), rgba(39,200,232,.7), rgba(39,200,232,.06)); transform-origin:left; }
  .bridge-node { width:7px; height:7px; border-radius:50%; background:#27C8E8; box-shadow:0 0 15px rgba(39,200,232,.75); flex:none; }
  .in-view .bridge-line { animation: line-grow 1.3s .45s ease both; }
  .in-view .bridge-node { animation: pulse 2.2s .65s ease-in-out infinite; }
  .network { position:absolute; width:38%; height:180px; right:2%; top:14%; opacity:.5; z-index:-1; pointer-events:none; }
  .network path { stroke:#27C8E8; stroke-width:1; fill:none; stroke-opacity:.35; }
  .network circle { fill:#43D8EE; opacity:.7; }
  .modern-quote { font-family: Georgia, "Times New Roman", serif; font-size:clamp(25px, 3vw, 41px); line-height:1.28; letter-spacing:-.75px; font-weight:400; color:#F7F8FC; margin:0; max-width:780px; }
  .em-data, .em-ai, .em-wisdom { color:#54D9EB; text-decoration:none; text-decoration-color:rgba(84,217,235,.65); text-underline-offset:5px; transition:color .2s ease, text-shadow .2s ease; outline-offset:5px; }
  .em-ai { color:#9BC8FF; }
  .em-wisdom { color:#E8C88F; }
  .em-data:hover, .em-data:focus-visible, .em-ai:hover, .em-ai:focus-visible, .em-wisdom:hover, .em-wisdom:focus-visible { text-decoration:underline; text-shadow:0 0 17px rgba(84,217,235,.22); }
  .signature { opacity:0; transform:translateY(10px); color:#C3D0E2; font-family:Georgia, "Times New Roman", serif; font-size:16px; font-style:italic; letter-spacing:.5px; margin-top:25px; }
  .in-view .signature { animation: rise .7s 1.75s ease forwards; }
  .closing-rule { margin-top:clamp(34px, 5vw, 60px); height:1px; background:linear-gradient(90deg, transparent, rgba(39,200,232,.4), rgba(211,175,111,.3), transparent); position:relative; }
  .closing-rule:after { content:""; position:absolute; width:4px; height:4px; left:50%; top:-1.5px; border-radius:50%; background:#71E5F3; box-shadow:0 0 12px #27C8E8; }
  .wisdom-endnote { text-align:center; margin-top:18px; color:#647894; font-size:9px; letter-spacing:2.3px; text-transform:uppercase; }
  @keyframes rise { to { opacity:1; transform:translateY(0); } }
  @keyframes line-grow { from { transform:scaleX(0); opacity:.25; } to { transform:scaleX(1); opacity:1; } }
  @keyframes pulse { 0%,100% { box-shadow:0 0 7px rgba(39,200,232,.45); } 50% { box-shadow:0 0 18px rgba(39,200,232,.95); } }
  @media (max-width: 720px) {
    .wisdom-shell { min-height:0; padding:30px 22px 28px; border-radius:18px; }
    .wisdom-grid { grid-template-columns:1fr; gap:4px; }
    .history { padding:8px 0 12px; }
    .historic-quote { font-size:34px; }
    .bridge { margin:18px 0 18px; }
    .modern { padding:8px 0 0; }
    .modern-quote { font-size:29px; line-height:1.3; }
    .network { width:75%; top:36%; right:-5%; opacity:.26; }
    .signature { margin-top:21px; }
    .closing-rule { margin-top:35px; }
  }
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration:.01ms !important; animation-iteration-count:1 !important; transition-duration:.01ms !important; scroll-behavior:auto !important; }
    .history, .modern, .signature { opacity:1; transform:none; }
  }
</style>
</head>
<body>
<section class="wisdom-shell" id="wisdom-experience" role="region" aria-label="The Evolution of Wisdom by Albert Davis">
  <svg class="network" viewBox="0 0 360 180" aria-hidden="true">
    <path d="M10 130 L70 80 L125 105 L177 35 L235 70 L300 25 L350 55 M70 80 L88 20 L177 35 M125 105 L160 155 L235 70 L270 140 L350 55 M235 70 L300 105"/>
    <circle cx="10" cy="130" r="3"/><circle cx="70" cy="80" r="3"/><circle cx="125" cy="105" r="2.5"/><circle cx="177" cy="35" r="3.5"/><circle cx="235" cy="70" r="3"/><circle cx="300" cy="25" r="2.5"/><circle cx="350" cy="55" r="3"/><circle cx="88" cy="20" r="2"/><circle cx="160" cy="155" r="2.5"/><circle cx="270" cy="140" r="2.5"/><circle cx="300" cy="105" r="2"/>
  </svg>
  <div class="wisdom-kicker">THE EVOLUTION OF WISDOM &nbsp;·&nbsp; BY ALBERT DAVIS</div>
  <div class="wisdom-grid">
    <div class="history">
      <div class="then-label">THEN · THE CLASSIC WISDOM</div>
      <blockquote class="historic-quote">“Knowledge is power.”</blockquote>
      <div class="historic-by">— Francis Bacon</div>
    </div>
    <div class="modern">
      <div class="now-label">NOW · THE MODERN PERSPECTIVE</div>
      <blockquote class="modern-quote">“Knowledge is power. <span class="em-data" tabindex="0" title="Data provides evidence">Data</span> is the evidence, <span class="em-ai" tabindex="0" title="AI helps turn evidence into intelligence">AI</span> is the intelligence, and <span class="em-wisdom" tabindex="0" title="Wisdom gives intelligence direction">wisdom</span> is knowing what to do with both.”</blockquote>
      <div class="signature">— Albert Davis</div>
    </div>
  </div>
  <div class="bridge" aria-hidden="true"><div class="bridge-line"></div><div class="bridge-node"></div></div>
  <div class="closing-rule" aria-hidden="true"></div>
  <div class="wisdom-endnote">Timeless wisdom · Modern intelligence · Human purpose</div>
</section>
<script>
(function () {
  const section = document.getElementById('wisdom-experience');
  if (!section) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    section.classList.add('in-view');
    return;
  }
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          section.classList.add('in-view');
          observer.unobserve(section);
        }
      });
    }, { threshold: 0.18 });
    observer.observe(section);
  } else {
    section.classList.add('in-view');
  }
})();
</script>
</body>
</html>''',
    height=790,
    scrolling=False,
)


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
