# AuditMind 📊
an ai assisstant that drafts audit memos and checks IFRS/IAS compliance from financial statements

![Python](https://img.shields.io/badge/python-3.11-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.25-brightgreen)
![FAISS](https://img.shields.io/badge/FAISS-1.7.4-orange)
![Audit Wizard](https://img.shields.io/badge/Audit%20Wizard-%F0%9F%94%8E-yellow)
![Data Geek](https://img.shields.io/badge/Data%20Geek-%F0%9F%A7%A1-red)


---

## what is AuditMind?

AuditMind is an AI assisstant designed to help auditors by **automatically drafting audit summaries** from client financial statements while checking compliance againt **IFRS/IAS accounting standards**

it generates structured memos highlighting risks, red flags, and missing disclosures, with citations to the releavent standards

---

## why it matters?

auditors spend countless hours manually reading financial statements and cross-checking against complex IFRS/IAS rules

AuditMind **saves time, improves consistency, and ensures tracebility** by linking findings directly to the applicable accounting standards

---

## how does it work?

1. **upload the document :** financial statments in PDF, excel or word

2. **parse & structure data :** core/ingestion handles extraction of tables and text

3. **standards retrieval :** IFRS/IAS paragraphs are embedded and stored in FAISS for fast retrieval

4. **analysis & rule checking:** hybrid LLM + python rules engine checks compliance, identifies red flags, and score risk

5. **memo generation:** produces structured JSON and a polished PDF memo

6. **interactive dashboard:** display findings, compliance scores, and allows memo download

---

## tech stack

- parsing : `pdfplumber`, `python-docx`, `openpyxl` 

- embeddings + vector DB : `sentence-transformers`, `faiss-cpu` 

- LLM : `transformers`, `torch`

- PDF export : `reportlab`

- dashboard : `streamlit`

---

## example

**query:** check IFRS 16 (leases) for apple in 2022

**output:**

- missing discount rate disclosure (IFRS 16, paragraph 26)

- red flag: impairement test not reported

- risk level: medium

---

## quickstart

1. clone the repo

```bash

git clone https://github.com/Youcef3939/AuditMind.git
cd AuditMind
```

2. create a virtual environment
```
python -m venv venv

source venv/bin/activate # linux/mac
```
venv\Scripts\activate # windows

3. install dependencies
```
pip install -r requirements.txt
```

4. run the dashboard

```
streamlit run dashboard/app.py
```

5. upload a financial statement, lean back and watch AuditMind work its magic!

---

## diagram

```mermaid
flowchart TD

subgraph group_group_dashboard["Dashboard"]
  node_node_dashboard_app["AuditMind UI<br/>streamlit entrypoint<br/>[app.py]"]
end

subgraph group_group_ingestion["Ingestion"]
  node_node_loader["Loader<br/>dispatch layer<br/>[loader.py]"]
  node_node_pdf_parser["PDF parser<br/>document parser<br/>[pdf_parser.py]"]
  node_node_docx_parser["DOCX parser<br/>document parser<br/>[docx_parser.py]"]
  node_node_excel_parser["Excel parser<br/>table parser<br/>[excel_parser.py]"]
end

subgraph group_group_standards["Standards KB"]
  node_node_standards_parser["Standards parser<br/>[parser.py]"]
  node_node_embedder["Embedder<br/>embedding builder<br/>[embedder.py]"]
  node_node_vector_store[("Vector store<br/>faiss index<br/>[vector_store.py]")]
  node_node_vector_search["Vector search<br/>retrieval layer<br/>[vector_search.py]"]
end

subgraph group_group_analysis["Analysis"]
  node_node_rules_engine["Rules engine<br/>deterministic checks<br/>[rules_engine.py]"]
  node_node_llm_pipeline["LLM pipeline<br/>semantic analysis<br/>[llm_pipeline.py]"]
  node_node_scoring(("Scoring<br/>[scoring.py]"))
end

subgraph group_group_output["Output"]
  node_node_formatter["Formatter<br/>[formatter.py]"]
  node_node_pdf_generator["PDF generator<br/>report renderer<br/>[pdf_generator.py]"]
end

subgraph group_group_data["Data"]
  node_node_raw_data["Sample docs<br/>input corpus"]
  node_node_standards_data[("Standards data<br/>knowledge corpus")]
  node_node_parsed_data["Parsed data<br/>intermediate artifact<br/>[parsed_data.json]"]
  node_node_output_files[("Exports<br/>generated artifacts")]
end

node_node_dashboard_app -->|"uploads"| node_node_loader
node_node_dashboard_app -->|"views report"| node_node_formatter
node_node_loader -->|"routes PDF"| node_node_pdf_parser
node_node_loader -->|"routes DOCX"| node_node_docx_parser
node_node_loader -->|"routes Excel"| node_node_excel_parser
node_node_pdf_parser -->|"writes extracted data"| node_node_parsed_data
node_node_docx_parser -->|"writes extracted data"| node_node_parsed_data
node_node_excel_parser -->|"writes extracted data"| node_node_parsed_data
node_node_standards_data -->|"loads standards"| node_node_standards_parser
node_node_standards_parser -->|"chunks to vectors"| node_node_embedder
node_node_embedder -->|"indexes"| node_node_vector_store
node_node_vector_store -->|"serves retrieval"| node_node_vector_search
node_node_parsed_data -->|"analyzes"| node_node_rules_engine
node_node_parsed_data -->|"analyzes"| node_node_llm_pipeline
node_node_vector_search -->|"supplies guidance"| node_node_rules_engine
node_node_vector_search -->|"supplies context"| node_node_llm_pipeline
node_node_rules_engine -->|"findings"| node_node_scoring
node_node_llm_pipeline -->|"findings"| node_node_scoring
node_node_scoring -->|"summarizes"| node_node_formatter
node_node_formatter -->|"renders"| node_node_pdf_generator
node_node_pdf_generator -->|"exports"| node_node_output_files

click node_node_dashboard_app "https://github.com/youcef3939/auditmind/blob/main/dashboard/app.py"
click node_node_loader "https://github.com/youcef3939/auditmind/blob/main/core/ingestion/loader.py"
click node_node_pdf_parser "https://github.com/youcef3939/auditmind/blob/main/core/ingestion/pdf_parser.py"
click node_node_docx_parser "https://github.com/youcef3939/auditmind/blob/main/core/ingestion/docx_parser.py"
click node_node_excel_parser "https://github.com/youcef3939/auditmind/blob/main/core/ingestion/excel_parser.py"
click node_node_standards_parser "https://github.com/youcef3939/auditmind/blob/main/core/standards/parser.py"
click node_node_embedder "https://github.com/youcef3939/auditmind/blob/main/core/standards/embedder.py"
click node_node_vector_store "https://github.com/youcef3939/auditmind/blob/main/core/standards/vector_store.py"
click node_node_vector_search "https://github.com/youcef3939/auditmind/blob/main/core/standards/vector_search.py"
click node_node_rules_engine "https://github.com/youcef3939/auditmind/blob/main/core/analysis/rules_engine.py"
click node_node_llm_pipeline "https://github.com/youcef3939/auditmind/blob/main/core/analysis/llm_pipeline.py"
click node_node_scoring "https://github.com/youcef3939/auditmind/blob/main/core/analysis/scoring.py"
click node_node_formatter "https://github.com/youcef3939/auditmind/blob/main/core/output/formatter.py"
click node_node_pdf_generator "https://github.com/youcef3939/auditmind/blob/main/core/output/pdf_generator.py"
click node_node_raw_data "https://github.com/youcef3939/auditmind/tree/main/data/raw"
click node_node_standards_data "https://github.com/youcef3939/auditmind/tree/main/data/standards"
click node_node_parsed_data "https://github.com/youcef3939/auditmind/blob/main/parsed_data.json"
click node_node_output_files "https://github.com/youcef3939/auditmind/tree/main/output_files"

classDef toneNeutral fill:#f8fafc,stroke:#334155,stroke-width:1.5px,color:#0f172a
classDef toneBlue fill:#dbeafe,stroke:#2563eb,stroke-width:1.5px,color:#172554
classDef toneAmber fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#78350f
classDef toneMint fill:#dcfce7,stroke:#16a34a,stroke-width:1.5px,color:#14532d
classDef toneRose fill:#ffe4e6,stroke:#e11d48,stroke-width:1.5px,color:#881337
classDef toneIndigo fill:#e0e7ff,stroke:#4f46e5,stroke-width:1.5px,color:#312e81
classDef toneTeal fill:#ccfbf1,stroke:#0f766e,stroke-width:1.5px,color:#134e4a
class node_node_dashboard_app toneBlue
class node_node_loader,node_node_pdf_parser,node_node_docx_parser,node_node_excel_parser toneAmber
class node_node_standards_parser,node_node_embedder,node_node_vector_store,node_node_vector_search toneMint
class node_node_rules_engine,node_node_llm_pipeline,node_node_scoring toneRose
class node_node_formatter,node_node_pdf_generator toneIndigo
class node_node_raw_data,node_node_standards_data,node_node_parsed_data,node_node_output_files toneTeal
```

---

## why was AuditMind born?

auditing is one of the most time intensive and repetitive parts of financial work

auditors spend endless hours reading financial statements, cross-checking IFRS/IAS standards and drafting memos; a process that is

- manual: high risk of oversight and inconsistencies

- repetetive: same checks done over and over again

- complex: IFRS/IAS standards run into thousands of pages

i asked myself this question; what if auditors had an assisstant that could do the heavy lifting, parsing financials, retrieving relevant standards, and drafting structured memos whole leaving the judgment calls to humans?

that's how AuditMind was born: a free open source ai assisstant that gives auditors **speed**, **accuracy**, and **tracebility** without replacing professional judgment

---

## contributing

- fork the repo & submit PRs

- add sample financiall statements for testing

- suggest additional IFRS/IAS rules or enhancements

---

AuditMind isn't just another AI project

it's built on the belief that auditors deserve smarter tools and clients deserve clearer trust

> AuditMind - because accuracy isn't optional
