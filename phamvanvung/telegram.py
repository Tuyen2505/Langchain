from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Hàm gửi tin nhắn đến Telegram
def send_telegram_message(chat_id, text):
    TELEGRAM_BOT_TOKEN = "7986783191:AAEOyMs7K8C9z19OAaLwQa3OSNC7JaQ_cLQ"
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(TELEGRAM_API_URL, json=payload)

# Gửi câu hỏi đến API của bạn và nhận câu trả lời
def get_ai_response(question):
    API_URL = "http://127.0.0.1:5002/generative_ai"
    payload = {"question": question}
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            return response.json().get("answer", "Không nhận được câu trả lời từ AI.")
        else:
            return "Lỗi khi gửi câu hỏi đến AI."
    except Exception as e:
        return f"Lỗi kết nối đến AI: {str(e)}"

@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    print(f"💬 Nhận tin nhắn từ Telegram: {data}")

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text_received = data["message"].get("text", "")

        print(f"📩 Tin nhắn từ user: {text_received}")

        if text_received:
            # Gửi câu hỏi đến AI
            ai_response = get_ai_response(text_received)
            # Gửi phản hồi về Telegram
            send_telegram_message(chat_id, ai_response)

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=6869)




#chạy lệnh này trong terminal để set webhook
#curl -F "url=https://xxxxx.ngrok.io/telegram-webhook" "https://api.telegram.org/bot<TOKEN>/setWebhook"
#curl -F "url=https://bd8a-118-71-173-160.ngrok-free.app/telegram-webhook" "https://api.telegram.org/bot7986783191:AAEOyMs7K8C9z19OAaLwQa3OSNC7JaQ_cLQ/setWebhook"
