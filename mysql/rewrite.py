from langchain_google_genai import ChatGoogleGenerativeAI


API_KEY = "AIzaSyC6h1sGMN1u3QkXBGBtiT2Ej6OOYaYcYWU"
model_name: str = "gemini-2.0-flash-exp"
llm = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=API_KEY,  
)


def rewrite_prompt(prompt):
    messages = [
        {"role": "system", "content": "Tôi chỉ viết lại prompt thành truy vấn sql, không trả lời bất kỳ câu hỏi nào, chỉ trong 1 câu, các bảng truy vấn bao gồm ao, quan, doanh thu"},
        ]
    prompt_template = f"""Lấy ra từ khóa tìm kiếm từ {prompt} và thay vào phần name dưới dạng: SELECT p.product_name, SUM(pv.quantity) AS total_quantity FROM products p JOIN product_variants pv ON p.product_id = pv.product_id WHERE p.product_name = 'name' GROUP BY p.product_name;. không sửa đổi format của câu truy vấn chỉ trả về đúng câu truy vấn không thêm ```sql```. 
        Ví dụ: SELECT p.product_name, SUM(pv.quantity) AS total_quantity FROM products p JOIN product_variants pv ON p.product_id = pv.product_id WHERE p.product_name = 'Áo thun thể thao nam Active ProMax' GROUP BY p.product_name;
    """
    messages.append({"role": "user", "content": prompt_template})
    llm_response = llm.invoke(messages)
    result = llm_response.content
    return result



# while True:
#     text_input = input("Nhập văn bản (hoặc 'exit' để thoát): ")
#     if text_input.lower() == 'exit':
#         break
#     result = rewrite_prompt(text_input)
#     print(result)