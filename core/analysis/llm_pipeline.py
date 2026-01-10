from core.standards.vector_search import VectorSearch  

class LLMPipeline:
    def __init__(self):
        self.vector_search = VectorSearch()
        self.vector_search.load_embeddings()  

    def analyze_report(self, report_text: str):
        summary = report_text.split(".")[0] + "."

        top_matches = self.vector_search.query(top_k=5)

        insights = []
        for match in top_matches:
            insights.append(f"report might be missing guidance from {match['standard_code']} paragraph {match['paragraph']}.")

        return summary, insights

if __name__ == "__main__":
    report = (
        "Financial statements shall present fairly the financial position, financial performance and cash flows of an entity. "
        "An entity shall disclose information that is relevant to an understanding of the financial statements, including significant accounting policies."
    )

    pipeline = LLMPipeline()
    summary, insights = pipeline.analyze_report(report)

    print("Summary:\n", summary)
    print("\nInsights:")
    for i in insights:
        print(i)
