from core.analysis.rules_engine import RulesEngine

class Scorer:
    def __init__(self, report_text: str):
        self.report_text = report_text
        self.rules_engine = RulesEngine(report_text)

    def compute_score(self, findings: list, insights: list) -> float:
        
        base_score = 100.0
        penalty_per_finding = 5.0  
        penalty_per_insight = 2.0  

        total_penalty = len(findings) * penalty_per_finding + len(insights) * penalty_per_insight
        compliance_score = max(0.0, base_score - total_penalty)  

        return compliance_score

    def run_scoring(self):

        findings = self.rules_engine.run_rules()

        insights = self.rules_engine.insights if hasattr(self.rules_engine, "insights") else []

        compliance_score = self.compute_score(findings, insights)

        return compliance_score, insights, findings
