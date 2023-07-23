from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import YoutubeLoader
from langchain.document_loaders import ArxivLoader
from langchain.schema.document import Document
from typing import List


class Loader:
    def __init__(self):
        self.loader = None
        self.data = None

    def load_from_url(self, url: str = "https://lilianweng.github.io/posts/2023-06-23-agent/",
                      **kwargs
                      ) -> List[Document]:
        self.loader = WebBaseLoader(url, **kwargs)
        self.data = self.loader.load()
        return self.data

    def load_from_youtube(self, video_id: str = "Unzc731iCUY",
                          **kwargs
                          ) -> List[Document]:
        self.loader = YoutubeLoader(video_id=video_id, **kwargs)
        self.data = self.loader.load()
        return self.data

    def load_from_arxiv(self, query: str, **kwargs):
        self.loader = ArxivLoader(query=query, **kwargs)
        self.data = self.loader.load()
        return self.data
