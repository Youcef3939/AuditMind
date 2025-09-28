import os
import sys
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Make sure we can import core/*
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.analysis.llm_pipeline import LLMPipeline
from core.analysis.rules_engine import RulesEngine
from core.analysis.scoring import Scorer
from core.output.formatter import format_report


# -------- PDF Generation --------
def generate_pdf(report_data, pdf_path="compliance_report.pdf"):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Compliance Report")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Compliance Score: {report_data.get('compliance_score', 'N/A')}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Summary:")
    y -= 20
    c.setFont("Helvetica", 10)
    for line in report_data.get("summary", "").split("\n"):
        c.drawString(50, y, line)
        y -= 15

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Insights:")
    y -= 20
    c.setFont("Helvetica", 10)
    for insight in report_data.get("insights", []):
        c.drawString(50, y, f"- {insight}")
        y -= 15

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Findings:")
    y -= 20
    c.setFont("Helvetica", 10)
    for finding in report_data.get("findings", []):
        c.drawString(50, y, f"- {finding.get('rule')}: {finding.get('issue')}")
        y -= 15

    c.save()


# -------- Streamlit Dashboard --------
st.set_page_config(page_title="AuditMind Dashboard", layout="wide")
st.title("📊 AuditMind – AI-Powered Compliance Analysis")

uploaded_file = st.file_uploader("Upload a Financial Report (PDF)", type=["pdf"])

if uploaded_file is not None:
    # --- Step 1: Extract report text ---
    report_text = uploaded_file.read().decode("latin-1", errors="ignore")[:5000]

    # --- Step 2: Run Pipeline ---
    llm_pipeline = LLMPipeline()

    rules_engine = RulesEngine(report_text)
    findings = rules_engine.run_rules()
    insights = rules_engine.insights

    scorer = Scorer(report_text)
    compliance_score = scorer.compute_score(findings, insights)

    summary = report_text[:400] + "..."

    report_data = {
        "summary": summary,
        "insights": insights,
        "findings": findings,
        "compliance_score": compliance_score,
    }

    # --- Step 3: Show Results ---
    st.subheader("Compliance Summary")
    st.metric("Compliance Score", compliance_score)

    st.subheader("Summary")
    st.write(summary)

    st.subheader("Insights")
    for i in insights:
        st.write(f"- {i}")

    st.subheader("Findings")
    if findings:
        for f in findings:
            st.write(f"- **{f['rule']}**: {f['issue']}")
    else:
        st.write("✅ No major findings detected.")

    # --- Step 4: Download PDF Report ---
    if st.button("📥 Generate PDF Report"):
        pdf_path = "compliance_report.pdf"
        generate_pdf(report_data, pdf_path)
        with open(pdf_path, "rb") as f:
            st.download_button("Download Report", f, file_name="compliance_report.pdf")
        st.success("PDF report generated!")