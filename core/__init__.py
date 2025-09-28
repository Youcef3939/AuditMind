"""
core package for AuditMind.

contains:
- standards: embedded standards, vector store and search
- analysis: LLM pipeline, rules engine, scoring
- output: report formatting and PDF generation
"""

# Expose key submodules for easier import
from .standards.vector_store import VectorStore
from .standards.vector_search import VectorSearch
from .analysis.llm_pipeline import LLMPipeline
from .analysis.rules_engine import RulesEngine
from .analysis.scoring import Scorer
from .output.pdf_generator import PDFGenerator

__all__ = [
    "VectorStore",
    "VectorSearch",
    "LLMPipeline",
    "RulesEngine",
    "Scorer",
    "PDFGenerator"
]
