# 🚀 FLOWMIND AI — Process Intelligence & Optimization

**Turn operational data into actionable process improvements.**

FLOWMIND AI is a Python-based process intelligence dashboard designed to help users analyze business workflows, identify operational bottlenecks, evaluate inefficiencies, and explore opportunities for process optimization.

By combining interactive analytics with explainable, rule-based recommendations, the project demonstrates how data-driven thinking can support better operational decisions.

🌐 **Live Demo:** [Launch FLOWMIND AI](https://ai-process-improvement-analyzer-cx26mas2z5qutcmlycm4j6.streamlit.app/)

📂 **GitHub Repository:** [ai-process-improvement-analyzer](https://github.com/albertdavis-AD/ai-process-improvement-analyzer)

---

## 📌 The Business Problem

Every business process has hidden costs.

Waiting time, repetitive work, rework, and unnecessary expenses can quietly reduce productivity and increase operating costs. These inefficiencies are not always obvious when teams look at individual activities in isolation.

FLOWMIND AI brings process-level data into one interactive dashboard to help users understand where time and money are being consumed, compare potential improvements, and prioritize areas that deserve attention.

## ✨ Key Features

### 📊 1. Executive Overview
- Explore process performance through interactive dashboards.
- Review processing time, waiting time, operating cost, and rework.
- Identify activities that may be contributing to operational inefficiency.

### 🔍 2. Process Intelligence
- Examine individual process steps and their operational metrics.
- Compare work hours against waiting hours.
- Analyze cost and rework patterns across workflow activities.

### 🧪 3. What-If Analysis
- Explore hypothetical changes to process performance.
- Understand how changes in selected assumptions may affect operational outcomes.
- Compare scenarios to support more informed improvement decisions.

### 💡 4. Explainable Recommendations
- Generate recommendations using process metrics and predefined decision rules.
- Highlight potential opportunities to reduce waiting, rework, and costs.
- Connect recommendations to observable process indicators.

### 📄 5. Management Reporting
- Generate a management-oriented process report.
- Export reports as PDF for review and communication.
- Present findings in a format suitable for operational discussions.

### 📂 6. Data Upload and Analysis
- Upload process data from CSV and Excel (XLSX) files.
- Analyze structured operational data using a consistent set of required fields.
- Explore detailed process-level information.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic and data processing |
| Streamlit | Interactive web application and dashboard |
| Pandas | Data manipulation and analysis |
| Plotly | Interactive data visualizations |
| ReportLab | PDF report generation |
| OpenPyXL | Excel file support |

## 🧠 How the Analysis Works

FLOWMIND AI uses process metrics and explainable, rule-based analysis to help surface operational improvement opportunities.

The workflow is:

1. **Import:** Load the sample process data or upload your own dataset.
2. **Analyze:** Examine processing time, waiting time, cost, and rework.
3. **Identify:** Highlight activities that may represent bottlenecks or inefficiencies.
4. **Simulate:** Explore hypothetical process changes using the What-If Analysis section.
5. **Recommend:** Review rule-based improvement suggestions.
6. **Report:** Generate a PDF report to communicate findings.

**Important:** The current recommendation engine is heuristic and rule-based. It is not a trained machine-learning model, and its outputs should be validated against actual business context before decisions are made.

## 🚀 Run the Project Locally

### Prerequisites

- Python 3.10 or later
- Git
- A modern web browser

### 1. Clone the repository

```bash
git clone https://github.com/albertdavis-AD/ai-process-improvement-analyzer.git
cd ai-process-improvement-analyzer
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## 📁 Expected Input Data

For custom CSV or XLSX uploads, prepare a dataset containing the following columns:

| Column | Description |
|---|---|
| `process_step` | Name of the process activity |
| `avg_work_hours` | Average time spent actively working on the step, in hours |
| `avg_wait_hours` | Average waiting time associated with the step, in hours |
| `avg_cost_inr` | Average cost associated with the step, in Indian rupees |
| `rework_rate_pct` | Rework rate expressed as a percentage |
| `activity_type` | Classification of the activity |

Example CSV structure:

```csv
process_step,avg_work_hours,avg_wait_hours,avg_cost_inr,rework_rate_pct,activity_type
Document Verification,2.5,12,450,8,Manual
Credit Check,1.5,6,300,4,Automated
Risk Review,3,18,900,12,Manual
```

Use representative, consistently defined metrics and ensure that the values and units are appropriate for your process.

## 🎯 Potential Use Cases

- Business process improvement
- Operational efficiency analysis
- Workflow bottleneck identification
- Cost and waiting-time analysis
- Process automation opportunity assessment
- Management reporting and decision support

## 🔮 Future Development Opportunities

Potential enhancements include:

- Integration with real operational databases and business systems.
- Historical trend analysis and process performance monitoring.
- More advanced process mining and workflow visualization.
- Predictive analytics using validated historical data.
- User-defined optimization objectives and scenario comparisons.
- Automated report scheduling and configurable reporting.

These are potential future enhancements, not claims about the current implementation.

## 👨‍💻 About the Project

FLOWMIND AI is a portfolio project exploring the intersection of **business process improvement, data analytics, Python development, and AI-assisted decision support**.

It demonstrates an approach to translating operational data into structured insights that business users can investigate and discuss.

**Author:** Albert Davis

- GitHub: [@albertdavis-AD](https://github.com/albertdavis-AD)
- Project Repository: [FLOWMIND AI](https://github.com/albertdavis-AD/ai-process-improvement-analyzer)
- Live Application: [Open Dashboard](https://ai-process-improvement-analyzer-cx26mas2z5qutcmlycm4j6.streamlit.app/)

## 📄 License

No license has been specified in this README. Review your intended sharing terms and add an appropriate `LICENSE` file before presenting the project as open source.

---

*Better process visibility. Smarter improvement decisions. Measurable operational thinking.*
