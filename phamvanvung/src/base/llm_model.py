import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

def get_hf_llm(model_name: str = "gemini-2.0-flash-exp",
               max_new_token=1280000000,
               **kwargs):

    # Đặt API Key (cần thay thế bằng API key thật của bạn)
    API_KEY = "AIzaSyC6h1sGMN1u3QkXBGBtiT2Ej6OOYaYcYWU"
    genai.configure(api_key=API_KEY)

    # Sử dụng LangChain với Gemini
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        max_output_tokens=max_new_token,
        google_api_key=API_KEY,  
        **kwargs
    )

    return llm

# llm = get_hf_llm()
# result = llm.invoke("What is the capital of France?")

# # Lấy chỉ nội dung câu trả lời
# answer = result.content

# print(answer)

# import torch
# from transformers import BitsAndBytesConfig
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# from langchain_huggingface import HuggingFacePipeline

# nf4_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_use_double_quant=True,
#     bnb_4bit_compute_dtype=torch.bfloat16
# )

# def get_hf_llm(model_name: str = "mistralai/Mistral-7B-Instruct-v0.2",
#             max_new_token = 1024,
#             **kwargs):
    
#     model = AutoModelForCausalLM.from_pretrained(
#         model_name,
#         quantization_config=nf4_config,
#         low_cpu_mem_usage=True
#     )

#     tokenizer = AutoTokenizer.from_pretrained(model_name)

#     model_pipeline = pipeline(
#         "text-generation",
#         model=model,
#         tokenizer=tokenizer,
#         max_new_tokens=max_new_token,
#         pad_token_id=tokenizer.eos_token_id,
#         device_map ="auto"
#     )

#     llm = HuggingFacePipeline(
#         pipeline = model_pipeline,
#         model_kwargs = kwargs
#     )

#     return llm




