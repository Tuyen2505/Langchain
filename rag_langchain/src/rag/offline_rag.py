import re
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

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
        self.prompt = hub.pull("rlm/rag-prompt")
        self.str_parser = Str_OutputParser()

    def get_chain(self, retriever):
        print(retriever)
        input_data = {
            "context":  RunnablePassthrough() | retriever.filter | self.format_docs,  # Gọi method thay vì dùng toán tử `|`
            "question": RunnablePassthrough()
        }

        rag_chain = (
            input_data
            | self.prompt
            | self.llm
            | self.str_parser
        )
        return rag_chain

    def format_docs(self, docs):
        # Thêm kiểm tra dữ liệu đầu vào
        if not isinstance(docs, dict) or "content" not in docs:
            raise ValueError("Invalid document format. Expected dict with 'content' key.")
            
        return "\n\n".join(docs["content"])

