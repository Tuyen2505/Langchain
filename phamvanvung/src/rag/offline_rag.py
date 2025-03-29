import re
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from src.rag.prompt import get_custom_rag_prompt

class Str_OutputParser(StrOutputParser):
    def __init__(self) -> None:
        super().__init__()

    def parse(self, text:str) -> str:
        return self.extract_answer(text)
    
    def extract_answer(self,
                    text_response:str,
                    pattern: str = r"Answer:\s*(.*)") -> str:

        match = re.search(pattern, text_response, re.DOTALL)
        if match:
            answer_text = match.group(1).strip()
            return answer_text
        else:
            return text_response


class Offline_RAG():
    def __init__(self, llm) -> None:
        self.llm = llm
        # self.prompt = hub.pull("rlm/rag-prompt")
        self.prompt = get_custom_rag_prompt()
        self.answer_only_prompt = ChatPromptTemplate.from_template(
            "Answer this question based on your knowledge:\nQuestion: {question}"
        )
        self.str_parser = Str_OutputParser()

    def get_chain(self, retriever):
        input_data = {
            "context":  RunnablePassthrough() | retriever.filter | self.format_docs,  # Gọi method thay vì dùng toán tử `|`
            "question": RunnablePassthrough()
        }

        # Kiểm tra context rỗng
        def is_empty_context(input_dict: dict) -> bool:
            return not input_dict["context"].strip()
        
        # Xử lý khi KHÔNG có context
        no_context_chain = (
            RunnableLambda(lambda x: {"question": x["question"]})  # Trích xuất question
            | self.answer_only_prompt                             # Prompt đơn giản
            | self.llm                                            # Truyền thẳng vào LLM
            | self.str_parser
        )

        # Xử lý khi CÓ context
        has_context_chain = (
            self.prompt  # Prompt gốc với context
            | self.llm
            | self.str_parser
        )

        # Phân nhánh xử lý
        branch = RunnableBranch(
            (is_empty_context, no_context_chain),  # Nhánh không có context
            has_context_chain                       # Nhánh mặc định
        )

        # Kết hợp tất cả thành chain hoàn chỉnh
        rag_chain = (
            input_data
            | branch
        )

        return rag_chain

    def format_docs(self, docs):
        # Thêm kiểm tra dữ liệu đầu vào
        if not isinstance(docs, dict) or "content" not in docs:
            raise ValueError("Invalid document format. Expected dict with 'content' key.")
            
        return "\n\n".join(docs["content"])


