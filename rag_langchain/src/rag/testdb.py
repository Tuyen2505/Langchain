from file_loader import Loader
import os

data_dir = "D:\\vscode\\Langchain\\rag_langchain\\data_source\\vietnam"

if __name__ == "__main__":
    doc_loader = Loader(file_type="pdf").load_dir(data_dir, workers=2)
    # page_contents = [doc.page_content for doc in doc_loader]
    # print(len(page_contents))
    # print(doc_loader[0].metadata["page_label"])
    # print(doc_loader[0].metadata["source"])
    # Lấy tên tệp từ đường dẫn
    source_path = doc_loader[0].metadata["source"]
    # Lấy tên tệp từ đường dẫn
    file_name = os.path.basename(source_path)

    # In kết quả
    print(file_name)

    # page_label = metadata.get('page_label')
    # source = metadata.get('source')
    # print("Page Label:", page_label)
    # print("Source:", source)