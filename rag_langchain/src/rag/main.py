from pydantic import BaseModel, Field

from src.rag.offline_rag import Offline_RAG
from src.rag.retrieval import Retriever

class InputQA(BaseModel):
    question: str = Field(...,title="The question to ask the model")

class OutputQA(BaseModel):
    answer: str = Field(...,title="Answer from the model")

def build_rag_chain(llm):
    retriever = Retriever()
    rag_chain = Offline_RAG(llm).get_chain(retriever)
    return rag_chain


    