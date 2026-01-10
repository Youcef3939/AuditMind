from core.standards.vector_search import VectorSearch

class RulesEngine:
    def __init__(self, report_text: str):
        self.report_text = report_text
        self.vector_search = VectorSearch()
        self.vector_search.load_embeddings()  
        self.insights = []  

    def run_rules(self) -> list:
        findings = []

        if "financial statements" not in self.report_text.lower():
            findings.append({
                "rule": "Financial Statements Check",
                "issue": "Missing reference to financial statements"
            })

        top_matches = self.vector_search.query(self.report_text, top_k=5)
        for match in top_matches:
            insight = f" report might be missing guidance from {match['standard_code']} paragraph {match['paragraph']}."
            self.insights.append(insight)

        return findings
