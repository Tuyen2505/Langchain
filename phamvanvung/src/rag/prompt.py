from langchain_core.prompts import ChatPromptTemplate

def get_custom_rag_prompt():
    """
    Tạo prompt template tùy chỉnh cho mô hình RAG.
    """
    return ChatPromptTemplate.from_template(
        """
        You are an AI assistant specialized in retrieving and answering questions based on provided context.
        Use the given context to answer the user's question accurately.
        If the answer is not available in the context, state that clearly.
        Provide a detailed response.

        Question: {question}
        Context: {context}
        Answer:
        """
    )

# Sử dụng prompt mới
custom_prompt = get_custom_rag_prompt()

# In ra nội dung của prompt
# print(custom_prompt)
