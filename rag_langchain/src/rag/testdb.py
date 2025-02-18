from file_loader import Loader


data_dir = "D:\\vscode\\Langchain\\rag_langchain\\data_source\\vietnam"

if __name__ == "__main__":
    doc_loader = Loader(file_type="pdf").load_dir(data_dir, workers=2)
    page_contents = [doc.page_content for doc in doc_loader]
    print(len(page_contents))