from transformers import BitsAndBytesConfig
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

def get_hf_llm(model_name: str = "mistralai/Mistral-7B-Instruct-v0.2",
            max_new_token = 1024,
            **kwargs):
    
    # Đặt API Key (cần thay thế bằng API key thật của bạn)
    API_KEY = "AIzaSyC6h1sGMN1u3QkXBGBtiT2Ej6OOYaYcYWU"
    genai.configure(api_key=API_KEY)


    model_pipeline = pipeline(
        "text-generation",
        model=model_name,
        tokenizer=tokenizer,
        max_new_tokens=max_new_token,
        pad_token_id=tokenizer.eos_token_id,
        device_map ="auto"
    )

    llm = HuggingFacePipeline(
        pipeline = model_pipeline,
        model_kwargs = kwargs
    )

    return llm





llm = get_hf_llm()

response = llm.invoke("Viết một bài thơ về mùa xuân.")
print(response)