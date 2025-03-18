from pathlib import Path
from typing import List
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_postgres.vectorstores import PGVector
from langchain_core.documents import Document
from langchain_community.embeddings import OpenAIEmbeddings
import os
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.chat_models import ChatOllama
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

embeddings = (
    OllamaEmbeddings(model="llama3.2")
    if os.getenv("MODEL") == "ollama"
    else OpenAIEmbeddings(model="text-embedding-3-large")
)
llm = ChatOllama(model="llama3.2") if os.getenv("MODEL") == "ollama" else ChatOpenAI()


def get_text_files(directory: str) -> List[Path]:
    return list(Path(directory).glob("*.txt"))


def load_docs() -> List[Document]:
    text_files = get_text_files("./docs")
    documents: List[Document] = []
    for file_path in text_files:
        loader = TextLoader(str(file_path))
        document = loader.load()
        documents = documents + document
    return documents


def indexting() -> None:
    documents = load_docs()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    connection_string = "postgresql+psycopg://postgres:postgres@localhost:5432/songs"

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name="songs",
        connection=connection_string,
        use_jsonb=True,
    )

    vector_store.add_documents(docs)


if __name__ == "__main__":
    indexting()
