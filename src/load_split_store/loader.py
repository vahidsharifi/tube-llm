from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import YoutubeLoader
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

    def load_from_youtube(self, video_id: str = "Unzc731iCUY"
                          ) -> List[Document]:
        self.loader = YoutubeLoader(video_id=video_id)
        self.data = self.loader.load()
        return self.data
