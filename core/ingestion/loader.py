import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ingestion import pdf_parser, excel_parser, docx_parser

SUPPORTED_EXTENSIONS = ['.pdf', '.xls', '.xlsx', '.docx']

def load_file(file_path):

    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.pdf':
        return pdf_parser.parse_pdf(file_path)
    elif ext in ['.xls', '.xlsx']:
        return excel_parser.parse_excel(file_path)
    elif ext == '.docx':
        return docx_parser.parse_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def load_all_files(raw_dir='data/raw'):

    all_data = {}
    for fname in os.listdir(raw_dir):
        full_path = os.path.join(raw_dir, fname)
        if os.path.isfile(full_path) and os.path.splitext(fname)[1].lower() in SUPPORTED_EXTENSIONS:
            print(f"Loading {fname}...")
            parsed = load_file(full_path)
            all_data[fname] = parsed
    return all_data

def print_summary(all_data):

    print(f"\nLoaded {len(all_data)} files.\n")
    for fname, parsed in all_data.items():
        print(f"{fname}:")
        if 'pages' in parsed:  
            print(f"  Pages: {len(parsed['pages'])}")
            print(f"  First page snippet: {parsed['pages'][0]['text'][:200]}...\n")
        elif 'sheets' in parsed:  
            total_tables = sum(len(s['tables']) for s in parsed['sheets'])
            print(f"  Sheets: {len(parsed['sheets'])}, Total tables: {total_tables}\n")
        elif 'paragraphs' in parsed:  
            print(f"  Paragraphs: {len(parsed['paragraphs'])}")
            print(f"  First paragraph: {parsed['paragraphs'][0]['text'][:200]}...\n")

if __name__ == "__main__":
    data = load_all_files()
    print_summary(data)
    
    with open("parsed_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Parsed data saved to parsed_data.json")
