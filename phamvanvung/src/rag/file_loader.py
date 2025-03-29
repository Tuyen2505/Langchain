import re
from typing import Union, List, Literal
import glob
from tqdm import tqdm
import multiprocessing
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

def load_pdf(pdf_file):
    """Đọc nội dung PDF tiếng Anh một cách đơn giản."""
    docs = PyPDFLoader(pdf_file).load()
    return docs

def get_num_cpu():
    return multiprocessing.cpu_count()

class BaseLoader:
    def __init__(self) -> None:
        self.num_processes = get_num_cpu()

    def __call__(self, files: List[str], **kwargs):
        pass

class PDFLoader(BaseLoader):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, pdf_files: List[str], **kwargs):
        num_processes = min(self.num_processes, kwargs["workers"])
        with multiprocessing.Pool(num_processes) as pool:
            doc_loaded = []
            total_files = len(pdf_files)
            with tqdm(total=total_files, desc="Loading PDFs", unit="file") as pbar:
                for result in pool.imap_unordered(load_pdf, pdf_files):
                    doc_loaded.extend(result)
                    pbar.update(1)
        return doc_loaded
    
class TextCleaner:
    """Lớp hỗ trợ làm sạch văn bản trước khi xử lý."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Xóa khoảng trắng dư thừa và chỉ giữ lại một khoảng trắng giữa các từ."""
        text = re.sub(r"\s+", " ", text)  # Thay thế nhiều khoảng trắng thành một
        return text.strip()

class TextSplitter:
    def __call__(self, documents):
        # Làm sạch văn bản trước khi chia nhỏ
        for doc in documents:
            doc.page_content = TextCleaner.clean_text(doc.page_content)
        
        # Hợp nhất tất cả nội dung từ các documents thành một chuỗi văn bản duy nhất
        combined_text = " ".join([doc.page_content for doc in documents])
        
        # Chia nhỏ theo Title mà vẫn giữ từ khóa
        pattern = r"(?=Title:?.*)"
        title_chunks = re.split(pattern, combined_text)
        title_chunks = [s.strip() for s in title_chunks if s.strip()]  # Xóa khoảng trắng dư và bỏ đoạn rỗng
            
        # Tạo lại các Document từ các đoạn chia
        split_docs = [Document(page_content=chunk) for chunk in title_chunks]
        
        return split_docs
    
class Loader:
    def __init__(self,
                file_type: str = Literal["pdf"],
                ) -> None:
        
        assert file_type in ["pdf"], "file_type must be pdf"
        self.file_type = file_type
        if file_type == "pdf":
            self.doc_loader = PDFLoader()
        else:
            raise ValueError("file_type must be pdf")
        
        self.doc_splitter = TextSplitter()

    def load(self, pdf_files: Union[str, List[str]], workers: int = 1):
        if isinstance(pdf_files, str):
            pdf_files = [pdf_files]
        doc_loaded = self.doc_loader(pdf_files, workers=workers)
        doc_split = self.doc_splitter(doc_loaded)
        return doc_split
    
    def load_dir(self, dir_path: str, workers: int = 1):
        if self.file_type == "pdf":
            files = glob.glob(f"{dir_path}/*.pdf")
            assert len(files) > 0, f"No {self.file_type} files found in {dir_path}"
        else:
            raise ValueError("file_type must be pdf")
        return self.load(files, workers)
