from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer

# Kết nối đến Milvus
connections.connect(alias="default", host="localhost", port="19530")

# Khởi tạo collection
collection_name = "test"
collection = Collection(collection_name)
collection.load()

# Load mô hình embedding
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

class Retriever:
    def __init__(self, search_type="L2") -> None:
        self.search_type = search_type

    def search_in_milvus(self, query_text, top_k=10):
        # Mã hóa câu nhập thành vector
        query_vector = model.encode([query_text]).tolist()
        # Truy vấn Milvus
        search_params = {"metric_type": self.search_type, "params": {"nprobe": 10}}
        results = collection.search(
            data=query_vector,
            anns_field="vectorDB",
            param=search_params,
            limit=top_k,
            output_fields=["my_varchar"]
        )
        return results
    
    def filter(self, query_text: str, threshold=1.3):
        results = self.search_in_milvus(query_text)
        data = {"content": [], "distance": []}
        
        for hit in results[0]:
            if hit.distance < threshold:
                data["content"].append(hit.get('my_varchar'))
                data["distance"].append(hit.distance)
        return data

# # Nhập câu truy vấn
# while True:
#     query_text = input("Nhập câu để tìm kiếm: ")
#     if query_text.lower() == "exit":
#         break
#     data = Retriever().filter(query_text)
#     print(data)
