from file_loader import Loader
from vectorstore import VectorDB

data_dir = "D:\\vscode\\Langchain\\rag_langchain\\data_source\\vietnam"

if __name__ == "__main__":
    doc_loader = Loader(file_type="pdf").load_dir(data_dir, workers=2)
    retriever = VectorDB(documents=doc_loader).get_retriever()
    results = retriever.invoke("Nguyên nhân chính dẫn đến tai nạn giao thông")

    # Lấy nội dung text từ các tài liệu
    text_results = [doc.page_content for doc in results]

    # In ra nội dung text
    for text in text_results:
        print(text)