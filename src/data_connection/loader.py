from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import YoutubeLoader
from langchain.document_loaders import ArxivLoader
from langchain.document_loaders import WikipediaLoader
from langchain.tools import YouTubeSearchTool
from langchain.schema.document import Document
import ast
from typing import List


class Loader:
    def __init__(self):
        self.loader = None
        self.data = None

    def load_from_url(self, url: str = "https://lilianweng.github.io/posts/2023-06-23-agent/",
                      **kwargs) -> List[Document]:
        self.loader = WebBaseLoader(url, **kwargs)
        self.data = self.loader.load()
        return self.data

    def load_from_youtube(self, video_id: str = "Unzc731iCUY", 
                          query: str = None, num_videos: int = 5,
                          **kwargs) -> List[Document]:
        if query is not None:
            tool = YouTubeSearchTool()
            urls = ast.literal_eval(tool.run(query + f" , {num_videos}"))
            self.data = []
            for url in urls:
                loader = YoutubeLoader.from_youtube_url("https://www.youtube.com" + url)
                self.data.extend(loader.load())
        else:
            self.loader = YoutubeLoader(video_id=video_id, **kwargs)
            self.data = self.loader.load()
        return self.data

    def load_from_arxiv(self, query: str,
                        **kwargs) -> List[Document]:
        self.loader = ArxivLoader(query=query, **kwargs)
        self.data = self.loader.load()
        return self.data

    def load_from_wikipedia(self, query: str,
                            **kwargs) -> List[Document]:
        self.loader = WikipediaLoader(query=query, **kwargs)
        self.data = self.loader.load()
        return self.data