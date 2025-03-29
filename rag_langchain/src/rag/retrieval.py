from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer
from langchain_core.runnables import chain
# Kết nối đến Milvus
#connections.connect(alias="default", host="milvus-standalone", port="19530")
connections.connect(alias="default", host="localhost", port="19530")

# Khởi tạo collection
collection_name = "vietnam"  # Thay thế bằng tên collection của bạn
collection = Collection(collection_name)
collection.load()
# Load mô hình embedding
model = SentenceTransformer("Cloyne/vietnamese-sbert-v3")

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
            output_fields=["my_varchar", "page", "source"]
        )
        return results
    
    def filter(self, query_text: str, threshold=130):
        results = self.search_in_milvus(query_text)
        data = {}
        content = []
        page = []
        source = []
        distance = []
        for hit in results[0]:
            if hit.distance < threshold:
                content.append(hit.get('my_varchar'))
                page.append(hit.get('page'))
                source.append(hit.get('source'))
                distance.append(hit.distance)
        data["content"] = content
        data["page"] = page
        data["source"] = source
        data["distance"] = distance
        return data
# Nhập câu truy vấn
while True:
    query_text = input("Nhập câu để tìm kiếm: ")
    if query_text == "exit":
        break
    data =   Retriever().filter(query_text)
    print(data)


