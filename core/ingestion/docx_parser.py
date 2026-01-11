from docx import Document

def parse_docx(file_path):

    doc = Document(file_path)
    output = {
        'file_name': file_path.split('/')[-1],
        'paragraphs': []
    }
    
    for idx, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if text:  
            output['paragraphs'].append({
                'index': idx,
                'text': text
            })
    
    return output

if __name__ == "__main__":
    parsed = parse_docx("data/raw/apple_test.docx")
    for p in parsed['paragraphs'][:5]:  
        print(f"{p['index']}: {p['text']}")
