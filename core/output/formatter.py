# core/output/formatter.py

def format_report(summary, insights, findings, compliance_score):
    """
    Formats the compliance report into a single string for display or PDF generation.
    """
    report = f"# Compliance Report\n\n"
    report += f"## Compliance Score: {compliance_score}\n\n"
    report += "## Summary:\n"
    report += f"{summary}\n\n"
    report += "## Insights:\n"
    for ins in insights:
        report += f"- {ins}\n"
    report += "\n## Findings:\n"
    for f in findings:
        report += f"- **{f['rule']}**: {f['issue']}\n"
    return report
    return {
        "compliance_score": compliance_score,
        "summary": summary,
        "insights": insights,
        "findings": findings
    }