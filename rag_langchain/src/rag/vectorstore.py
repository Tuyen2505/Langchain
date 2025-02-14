from typing import Union
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer

model_name = "Cloyne/vietnamese-sbert-v3"
model = SentenceTransformer(model_name)
embedding_model = HuggingFaceEmbeddings(model_name = model_name)

class VectorDB:

    def __init__(self,
                documents = None,
                vector_db: Union[Chroma, FAISS] = Chroma,
                embedding = embedding_model,
                ) -> None:
        
        self.vector_db = vector_db
        self.embedding = embedding
        self.db = self._build_db(documents)
    
    def _build_db(self, documents):
        db = self.vector_db.from_documents(documents = documents, embedding = self.embedding)
        return db
    
    def get_retriever(self,
                    search_type: str = "similarity",
                    search_kwargs: dict = {"k": 10}
                    ):
        
        retriever = self.db.as_retriever(search_type = search_type, search_kwargs = search_kwargs)
        return retriever

