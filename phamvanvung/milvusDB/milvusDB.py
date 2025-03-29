from pymilvus import MilvusClient, DataType
from sentence_transformers import SentenceTransformer

import sys
import os
# Lấy thư mục cha chứa cả VectorDB và rag_langchain
parent_dir = os.path.abspath("..")
sys.path.append("D:/vscode/Langchain/phamvanvung")  # Thêm vào sys.path
from src.rag.file_loader import Loader


# 1. Kết nối Milvus :cite[1]:cite[9]
client = MilvusClient(
    uri="http://localhost:19530",  # Địa chỉ Milvus server
    token="root:Milvus"            # Thông tin xác thực
)

# 2. Tạo collection với schema tùy chỉnh :cite[4]:cite[8]
collection_name = "pdf_collection"
dimension = 768  

schema = client.create_schema(
    auto_id=True,
    enable_dynamic_field=False
)

schema.add_field(
    field_name="id", 
    datatype=DataType.INT64, 
    is_primary=True
)
schema.add_field(
    field_name="vectorDB", 
    datatype=DataType.FLOAT_VECTOR, 
    dim=dimension
)
schema.add_field(
    field_name="my_varchar", 
    datatype=DataType.VARCHAR, 
    max_length=65535
)
client.create_collection(
    collection_name=collection_name,
    schema=schema
)

# Tạo index cho trường vectorDB

index_params = MilvusClient.prepare_index_params()

index_params.add_index(
    field_name="vectorDB",
    metric_type="L2",
    index_type="IVF_FLAT",
    index_name="vector_index",
    params={ "nlist": 128 }
)

client.create_index(
    collection_name=collection_name,
    index_params=index_params,
    timeout=30,
    sync=False # Whether to wait for index creation to complete before returning. Defaults to True.
)



# 3. Khởi tạo embedding model
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# 4. Xử lý file PDF và chèn vào Milvus
def insert_pdf_to_milvus(data_dir,data_type):
    doc_loader = Loader(file_type=data_type).load_dir(data_dir, workers=2)
    chunks = [doc.page_content for doc in doc_loader]
    embeddings = model.encode(chunks)

    
    # Chuẩn bị dữ liệu để chèn, thêm thuộc tính chunk_overlap
    data = [
        {
            "vectorDB": emb.tolist(),
            "my_varchar": chunk,
        } 
        for emb, chunk in zip(embeddings, chunks)
    ]
    
    # Thực hiện insert vào collection (giả sử client và collection_name đã được khởi tạo)
    insert_result = client.insert(
        collection_name=collection_name,
        data=data
    )
    
    print(f"Đã chèn {len(insert_result['ids'])} bản ghi thành công từ folder: {data_dir}!")
    return insert_result


# 5. Thực thi chương trình
if __name__ == "__main__":
    data_dir = "D:/vscode/Langchain/phamvanvung/data_source/generative_ai"
    data_type = "pdf"
    result = insert_pdf_to_milvus(data_dir, data_type)