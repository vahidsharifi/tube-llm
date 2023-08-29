from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.document import Document
from typing import List


class Store:
    def __init__(self, embedding=OpenAIEmbeddings()):
        self.embedding = embedding

    def store_data(self, splits: List[Document]):
        vectorstore = Chroma.from_documents(documents=splits, embedding=self.embedding)
        return vectorstore
