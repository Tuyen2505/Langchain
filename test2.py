doc_loader = Loader(file_type=data_type).load_dir(data_dir, workers=2)
retriever = VectorDB(documents = doc_loader).get_retriever()