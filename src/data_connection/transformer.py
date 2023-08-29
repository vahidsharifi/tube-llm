from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from typing import List


class Transformer:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

    def split_data(self, data: List[Document]) -> List[Document]:
        all_splits = self.text_splitter.split_documents(data)
        return all_splits


if __name__ == '__main__':
    from loader import Loader

    d = Loader().load_from_url()
    s = Split().split_data(d)
    print(s)
    print(type(s[0]))
