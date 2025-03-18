from pathlib import Path
from typing import List
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document
from langchain_community.embeddings import OpenAIEmbeddings
import os
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.chat_models import ChatOllama
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

embeddings = (
    OllamaEmbeddings(model="llama3.2") if os.getenv("MODEL") == "ollama" else OpenAIEmbeddings()
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


def indexting():
    documents = load_docs()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    connection_string = "postgresql+psycopg2://postgres:postgres@localhost:5432/songs"

    db = PGVector.from_documents(
        embedding=embeddings,
        documents=docs,
        connection_string=connection_string,
        collection_name="songs",
    )

    db.add_documents(docs)
    return db


if __name__ == "__main__":
    indexting()
