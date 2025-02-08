from pydantic import BaseModel, Field

from src.rag.file_loader import Loader
from src.rag.vectorstore import VectorDB
from src.rag.offline_rag import Offline_RAG

class InputQA(BaseModel):
    question: str = Field(...,title="The question to ask the model")

class OutputQA(BaseModel):
    answer: str = Field(...,title="Answer from the model")

def build_rag_chain(llm, data_dir, data_type):
    doc_loader = Loader(file_type=data_type).load_dir(data_dir, workers=2)
    retriever = VectorDB(documents = doc_loader).get_retriever()
    rag_chain = Offline_RAG(llm).get_chain(retriever)

    return rag_chain


