# from google import genai
# from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

# client = genai.Client(api_key="AIzaSyC6h1sGMN1u3QkXBGBtiT2Ej6OOYaYcYWU")
# model_id = "gemini-2.0-flash"

# google_search_tool = Tool(
#     google_search = GoogleSearch()
# )

# response = client.models.generate_content(
#     model=model_id,
#     contents="Hôm nay là thứ mấy",
#     config=GenerateContentConfig(
#         tools=[google_search_tool],
#         response_modalities=["TEXT"],
#     )
# )

# for each in response.candidates[0].content.parts:
#     print(each.text)
# # Example response:
# # The next total solar eclipse visible in the contiguous United States will be on ...

# # To get grounding metadata as web content.
# print(response.text)


import requests

def google_search(query, api_key, cx):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cx
    }
    response = requests.get(url, params=params)
    return response.json()

results = google_search("top AI trends 2023", "AIzaSyAmt4Qq89b2FCUifi5ILurSwXshxNWLi5g", "jovial-valve-452002-u8")
print(results)