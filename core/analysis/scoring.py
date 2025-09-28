from core.analysis.rules_engine import RulesEngine

class Scorer:
    def __init__(self, report_text: str):
        self.report_text = report_text
        self.rules_engine = RulesEngine(report_text)

    def compute_score(self, findings: list, insights: list) -> float:
        """
        Computes a simple compliance score based on findings and insights.
        The more issues, the lower the score.
        Returns a float between 0 and 100.
        """
        base_score = 100.0
        penalty_per_finding = 5.0  # each finding reduces score
        penalty_per_insight = 2.0  # each insight reduces score

        total_penalty = len(findings) * penalty_per_finding + len(insights) * penalty_per_insight
        compliance_score = max(0.0, base_score - total_penalty)  # don't go below 0

        return compliance_score

    def run_scoring(self):
        """
        Run rules engine and scoring together.
        Returns a tuple: (compliance_score, insights, findings)
        """
        # Run rules engine
        findings = self.rules_engine.run_rules()

        # Gather insights (LLM insights should already be passed externally)
        insights = self.rules_engine.insights if hasattr(self.rules_engine, "insights") else []

        # Compute compliance score
        compliance_score = self.compute_score(findings, insights)

        return compliance_score, insights, findings
