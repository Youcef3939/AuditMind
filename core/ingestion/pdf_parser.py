import pdfplumber
import re

def clean_text(text):
    """basic cleanup: remove excessive whitespace and line breaks"""
    text = re.sub(r'\n+', '\n', text)
    text = text.strip()
    return text

def parse_pdf(file_path):
    """
    parse a PDF file and return structured text + tables
    Returns:
        dict: {
            'file_name': str,
            'pages': [
                {'page_number': int,
                 'text': str,
                 'tables': list of 2D lists}
                ]
        }
    """
    output = {
        'file_name': file_path.split('/')[-1],
        'pages': []
    }

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text() or ""
            page_text = clean_text(page_text)

            page_tables = []
            for table in page.extract_tables():
                page_tables.append(table)

            output['pages'].append({
                'page_number': i,
                'text': page_text,
                'tables': page_tables
            })

    return output

# test
if __name__ == "__main__":
    parsed = parse_pdf("data/raw/apple_2023.pdf")
    print(parsed['pages'][0]['text'][:500])  