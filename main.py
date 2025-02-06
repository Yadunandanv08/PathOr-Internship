import sys
import os
import time
import psutil
from processor import parallel_pdf_process
from excel_processor import extract_excel
from chunking import ChunkManager
from query_handler import queryModel

def memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  

def measure_performance(file_path):
    start_time = time.time()

    initial_memory = memory_usage()
    print(f"Initial Memory Usage: {initial_memory:.2f} MB")
    
    chunks = process_file(file_path)
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time:.2f} seconds")

    final_memory = memory_usage()
    print(f"Final Memory Usage: {final_memory:.2f} MB")

    return chunks

def process_file(file_path):
    manager = ChunkManager()
    if file_path.endswith('.pdf'):
        processed = parallel_pdf_process(file_path)
        for page in processed:
            manager.add_content(page['text'], {'type': 'pdf', 'page': page['page']})
    elif file_path.endswith('.xlsx'):
        data = extract_excel(file_path)
        manager.add_content(data, {'type': 'excel'})
    return manager.chunks

if __name__ == '__main__':
    file_path = input("Enter file path:")
    
    chunks = measure_performance(file_path)
    
    engine = queryModel(chunks)
    
    while True:
        question = input("\nAsk your question: ").strip()
        if question.lower() in ['exit', 'quit']:
            break
        print(f"\nRESPONSE:\n{engine.query(question)}\n")
