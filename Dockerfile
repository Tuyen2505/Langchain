FROM python:3.10.10-slim
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential wget tar && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/milvus-io/milvus/releases/download/v2.0.2/milvus-standalone-docker-compose.yml -O docker-compose.ymls

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./rag_langchain ./rag_langchain

EXPOSE 2505

CMD ["python" , "milvusDB/milvusDB.py" && "python", "rag_langchain/server.py"]