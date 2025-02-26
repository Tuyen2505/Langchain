import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

# Khởi tạo công cụ tìm kiếm Google
google_search_tool = Tool(
    google_search=GoogleSearch()
)

def get_hf_llm_websearch(model_name: str = "gemini-2.0-flash-exp",
                         max_new_token: int = 1024,
                         **kwargs):
    # Đặt API Key (hãy thay thế bằng API Key thật của bạn)
    API_KEY = "AIzaSyC6h1sGMN1u3QkXBGBtiT2Ej6OOYaYcYWU"
    genai.configure(api_key=API_KEY)

    # Cấu hình GenerateContentConfig với công cụ tìm kiếm
    config = GenerateContentConfig(
        tools=[google_search_tool],
        response_modalities=["TEXT"],
        **kwargs
    )

    # Khởi tạo LLM sử dụng LangChain với Gemini
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        max_output_tokens=max_new_token,
        google_api_key=API_KEY,
        config=config
    )
    return llm

llm = get_hf_llm_websearch()
result = llm.invoke("Hôm nay là thứ mấy?")

# Lấy chỉ nội dung câu trả lời
answer = result.content

print(answer)