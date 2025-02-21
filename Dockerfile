FROM python:3.10.10-slim
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*


COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./milvusDB ./milvusDB
COPY ./rag_langchain ./rag_langchain

EXPOSE 2505

CMD ["python", "rag_langchain/server.py"]   