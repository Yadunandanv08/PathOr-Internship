from multiprocessing import Pool
import pdf_processor

def parallel_pdf_process(pdf_path):
    with Pool() as pool:
        results = pool.map(process_page, pdf_processor.extract_pages(pdf_path))
    return results

def process_page(page):
    page['text'] = f"Page {page['page']}:\n{page['text']}"
    if page['tables']:
        page['text'] += f"\nTables:\n{page['tables']}"
    return page