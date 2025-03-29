import requests

response = requests.get("http://127.0.0.1:6868/get-latest-message")
data = response.json()
print(f"{data['latest_text']}")