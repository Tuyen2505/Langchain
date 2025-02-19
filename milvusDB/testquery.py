from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer
from langchain_core.runnables import chain
# Kết nối đến Milvus
connections.connect(alias="default", host="localhost", port="19530")

# Khởi tạo collection
collection_name = "pdf_collection"  # Thay thế bằng tên collection của bạn
collection = Collection(collection_name)
collection.load()
# Load mô hình embedding
model = SentenceTransformer("Cloyne/vietnamese-sbert-v3")
# class Retriever:
    # def __init__(self, query_text,search_type="L2") -> None:
    #     self.query_text = query_text
    #     self.search_type = search_type

    # def search_in_milvus(self, top_k=10, threshold=90):
    #     # Mã hóa câu nhập thành vector
    #     query_vector = model.encode([self.query_text]).tolist()
        
    #     # Truy vấn Milvus để lấy 10 vector gần nhất
    #     search_params = {"metric_type": self.search_type, "params": {"nprobe": 10}}
    #     results = collection.search(
    #         data=query_vector,
    #         anns_field="vectorDB",  # Thay thế bằng tên trường vector trong collection
    #         param=search_params,
    #         limit=top_k,
    #         output_fields=["my_varchar"]  # Trả về cả nội dung gốc
    #     )
        
    #     # Hiển thị kết quả
    #     # for hit in results[0]:
    #     #     print(f"Score: {hit.distance:.4f}, Content: {hit.get('my_varchar')}")
    #     return results

#["id: 456090082827347287, distance: 105.60711669921875, entity: {\'my_varchar\': \'Tôi là Capybara – Vua c ủ a thế gi ớ i g ặ m nhấm!\\\\nXin chào! Tôi là Capybara, loài g ặ m m nhấm l ớ n nhất trên Trái Đất. Tôi thu ộ c h ọ  hàng nhà chu ộ t \\\\nlang nh ư ng l ạ i có kích th ướ c v ượ t tr ộ i: dài kho ả ng 1,2 mét, cao 50 cm và n ặ ng t ừ  35 - 65 kg. \\  \\\nTôi trông giống m ộ t chú l ợ n nh ỏ  nh ư ng l ạ i có khuôn m ặ t hiề n lành và đôi mắt tròn đáng yêu.\'}
    # def filter(self):
    #     results = self.search_in_milvus()
    #     data = {}
    #     content = []
    #     for hit in results[0]:
    #         content.append(hit.get('my_varchar'))
    #     data["content"] = content
    #     return data

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

    # def filter(self, query_text: str):
    #     results = self.search_in_milvus(query_text)
    #     print(results)
    #     content = [hit.get('my_varchar') for hit in results]
    #     return {"content": content}
    
    def filter(self, query_text: str, threshold=130):
        results = self.search_in_milvus(query_text)
        data = {}
        content = []
        page = []
        source = []
        for hit in results[0]:
            if hit.distance < threshold:
                content.append(hit.get('my_varchar'))
                page.append(hit.get('page'))
                source.append(hit.get('source'))
        data["content"] = content
        data["page"] = page
        data["source"] = source
        return data
# # Nhập câu truy vấn
while True:
    query_text = input("Nhập câu để tìm kiếm: ")
    if query_text == "exit":
        break
    data =   Retriever().filter(query_text)
    print(data)
    # print(data["content"])
    # print(data["source"])


