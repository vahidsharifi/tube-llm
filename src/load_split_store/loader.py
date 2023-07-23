from langchain.document_loaders import WebBaseLoader
from langchain.schema.document import Document
from typing import List


class Loader:
    def __init__(self):
        self.loader = None
        self.data = None

    def load_from_url(self, url: str = "https://lilianweng.github.io/posts/2023-06-23-agent/"
                      ) -> List[Document]:
        self.loader = WebBaseLoader(url)
        self.data = self.loader.load()
        return self.data


if __name__ == "__main__":
    l = Loader()
    d = l.load_from_url()
    print(d)
    print(type(d[0]))
