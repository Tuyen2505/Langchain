import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from langserve import add_routes

from src.base.llm_model import get_hf_llm
from src.rag.main import build_rag_chain, InputQA, OutputQA

llm = get_hf_llm(temperature=0.9)
genai_docs = "./data_source/vietnam"

# genai_chain = build_rag_chain(llm, data_dir=genai_docs, data_type="pdf")
genai_chain = build_rag_chain(llm)


app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="Langchain Server API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# ------------------ Routes ------------------

@app.get("/check")
async def check():
    return {"status": "ok"}

@app.post("/generative_ai", response_model=OutputQA) 
async def generative_ai(inputs: InputQA):
    answer = genai_chain.invoke(f"Trả lời bằng tiếng Việt: {inputs.question}")
    return {"answer": answer}

#------------------ Langserver Routes ------------------
add_routes(app,
        genai_chain,
        playground_type="default",
        path="/generative_ai")


