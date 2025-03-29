from flask import Flask, request, jsonify
import requests
from connectSQL import query_mysql
from rewrite import rewrite_prompt
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

app = Flask(__name__)

# 🔒 Danh sách ID Telegram được phép sử dụng bot
ALLOWED_USERS = {5982446232}  # Thay bằng ID của bạn

# 🔑 Khởi tạo Gemini AI
API_KEY = "AIzaSyC6h1sGMN1u3QkXBGBtiT2Ej6OOYaYcYWU"
model_name = "gemini-2.0-flash-exp"
llm = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=API_KEY,  
)

# 🤖 Hàm xử lý tin nhắn
def chatbot_response(user_query):
    sql_query = rewrite_prompt(user_query)  # Chuyển đổi câu hỏi thành SQL
    db_results = query_mysql(sql_query)

    if not db_results:
        return "❌ Xin lỗi, không tìm thấy kết quả phù hợp."

    # Định dạng dữ liệu MySQL
    formatted_data = "\n".join([
        ", ".join(f"{key}: {value}" for key, value in row.items()) 
        for row in db_results
    ])

    # Tạo prompt cho LLM
    prompt = PromptTemplate(
        input_variables=["user_query", "formatted_data"],
        template="""
        Người dùng hỏi: {user_query}
        Dữ liệu từ MySQL:
        {formatted_data}
        
        Hãy tạo câu trả lời tự nhiên dựa trên dữ liệu trên.
        """
    )

    # Gửi prompt đến Gemini
    response = llm.invoke(prompt.format(user_query=user_query, formatted_data=formatted_data))
    return response.content


# 📩 Xử lý webhook từ Telegram
@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    print(f"💬 Nhận tin nhắn từ Telegram: {data}")

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_id = data["message"]["from"]["id"]  # Lấy ID người gửi
        text_received = data["message"]["text"]

        # 🚫 Kiểm tra quyền sử dụng bot
        if user_id not in ALLOWED_USERS:
            print(f"❌ Người dùng {user_id} không có quyền sử dụng bot!")
            send_telegram_message(chat_id, "🚫 Bạn không có quyền sử dụng bot này.")
            return jsonify({"status": "forbidden"}), 200

        print(f"📩 Tin nhắn từ user: {text_received}")

        # ✅ Gọi chatbot xử lý tin nhắn
        response_text = chatbot_response(text_received)
        print(f"🤖 Chatbot trả lời: {response_text}")

        # 📤 Gửi tin nhắn phản hồi về Telegram
        send_telegram_message(chat_id, response_text)

    return jsonify({"status": "ok"}), 200


# 📤 Hàm gửi tin nhắn Telegram
def send_telegram_message(chat_id, text):
    TELEGRAM_BOT_TOKEN = "7962908225:AAGnoPTdw6dIuPt6C1uiSG0cIU-EoalM768"
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(TELEGRAM_API_URL, json=payload)


if __name__ == "__main__":
    app.run(port=6868)



#chạy lệnh này trong terminal để set webhook
#curl -F "url=https://xxxxx.ngrok.io/telegram-webhook" "https://api.telegram.org/bot<TOKEN>/setWebhook"
