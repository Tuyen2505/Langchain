# from pymilvus import connections, Collection, utility

# # Kết nối tới Milvus
# connections.connect(alias="default", host="localhost", port="19530")
# print(utility.list_collections())

# # Kết nối đến collection
# collection = Collection("pdf_collection")

# # # Nếu chưa có index, tạo index cho trường vectorDB
# # index_params = {
# #     "metric_type": "L2",         # Hoặc "IP" nếu dùng cosine similarity
# #     "index_type": "IVF_FLAT",      # Kiểu index, điều chỉnh theo nhu cầu
# #     "params": {"nlist": 128}
# # }
# # collection.create_index(field_name="vectorDB", index_params=index_params)
# # print("Index đã được tạo thành công!")

# # Load collection vào bộ nhớ
# collection.load()
# print("Collection đã được load vào bộ nhớ!")

# # Thực hiện truy vấn bao gồm trường vectorDB
# data = collection.query(expr="id >= 0", output_fields=["id", "vectorDB"], limit=10)
# print(data)