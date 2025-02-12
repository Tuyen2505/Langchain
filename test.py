import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

def get_hf_llm(model_name: str = "gemini-2.0-flash-exp",
               max_new_token=1024,
               **kwargs):

    # Đặt API Key (cần thay thế bằng API key thật của bạn)
    API_KEY = "AIzaSyC6h1sGMN1u3QkXBGBtiT2Ej6OOYaYcYWU"
    genai.configure(api_key=API_KEY)

    # Sử dụng LangChain với Gemini
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.7,
        max_output_tokens=max_new_token,
        google_api_key=API_KEY,  # ⚠️ API Key phải truyền vào đây
        **kwargs
    )

    return llm


llm = get_hf_llm()

response = llm.invoke("Viết một bài thơ về mùa xuân.")
print(response)