import PyPDF2
import re

def extract_pages(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            tables = _extract_tables(text)
            yield {'text': text, 'tables': tables, 'page': i+1}

def _extract_tables(text):
    lines = text.split('\n')
    table_data = []
    for line in lines:
        if re.match(r'(\s{2,}.+)+', line):
            cleaned = re.sub(r'\s{2,}', '|', line.strip())
            table_data.append(cleaned)
    return '\n'.join(table_data) if table_data else ''