from flask import Flask, request, jsonify

app = Flask(__name__)

from src.base.llm_model import get_hf_llm
#from src.base.web_search import get_hf_llm_websearch
from src.rag.main import build_rag_chain

llm = get_hf_llm(temperature=0.9)
genai_docs = "./data_source/vietnam"
genai_chain = build_rag_chain(llm)

@app.route("/generative_ai", methods=["POST"])
def generative_ai():
    data = request.get_json()
    # Lấy câu hỏi từ payload JSON (ví dụ: {"question": "Nội dung câu hỏi"})
    question = data.get("question", "")
    # Gọi hàm xử lý để lấy câu trả lời
    answer = genai_chain.invoke(f"Trả lời bằng tiếng Việt: {question}")
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)