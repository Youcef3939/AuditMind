from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from pathlib import Path
# from core.output.formatter import format_report

OUTPUT_DIR = Path("output_files")
OUTPUT_DIR.mkdir(exist_ok=True)

class PDFGenerator:
    def __init__(self, formatted_report: dict, filename: str = "compliance_report.pdf"):
        self.report = formatted_report
        self.filename = filename

    def save_pdf(self):
        pdf_path = OUTPUT_DIR / self.filename
        doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        elements.append(Paragraph("Compliance Report", styles['Title']))
        elements.append(Spacer(1, 12))

        # Compliance Score
        score = self.report.get("compliance_score", "N/A")
        elements.append(Paragraph(f"Compliance Score: {score}", styles['Heading2']))
        elements.append(Spacer(1, 12))

        # Summary
        elements.append(Paragraph("Summary:", styles['Heading2']))
        elements.append(Paragraph(self.report.get("summary", ""), styles['Normal']))
        elements.append(Spacer(1, 12))

        # Insights
        insights = self.report.get("insights", [])
        if insights:
            elements.append(Paragraph("Insights:", styles['Heading2']))
            for insight in insights:
                elements.append(Paragraph(f"- {insight}", styles['Normal']))
            elements.append(Spacer(1, 12))

        # Findings
        findings = self.report.get("findings", [])
        if findings:
            elements.append(Paragraph("Findings:", styles['Heading2']))
            for f in findings:
                elements.append(Paragraph(f"- {f.get('rule', '')}: {f.get('issue', '')}", styles['Normal']))
            elements.append(Spacer(1, 12))

        doc.build(elements)
        print(f"PDF saved at: {pdf_path.resolve()}")

# Example usage
if __name__ == "__main__":
    # Dummy report
    dummy_report = {
        "summary": "The company presents its financial position clearly.",
        "insights": ["⚠️ report might be missing guidance from ias1_presentation paragraph 10."],
        "findings": [{"rule": "Financial Statements Check", "issue": "Missing reference to financial statements"}],
        "compliance_score": 85.0
    }

    # If format_report is unavailable, use dummy_report directly
    pdf_gen = PDFGenerator(dummy_report)
    pdf_gen.save_pdf()