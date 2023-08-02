from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import YoutubeLoader
from langchain.document_loaders import ArxivLoader
from langchain.document_loaders import WikipediaLoader
from langchain.tools import YouTubeSearchTool
from langchain.schema.document import Document
import ast
from typing import List
import re
from urllib.parse import urlparse, parse_qs

class Loader:
    def __init__(self):
        self.loader = None
        self.data = None
        self.languages = ["af", "ak", "am", "ar", "as", "ay", "az", "be", "bg",
                          "bho", "bn", "bs", "ca", "ceb", "co", "cs", "cy", "da",
                          "de", "dv", "ee", "el", "en", "en-GB", "eo", "es", "et",
                          "eu", "fa", "fi", "fil", "fr", "fy", "ga", "gd", "gl",
                          "gn", "gu", "ha", "haw", "hi", "hmn", "hr", "ht", "hu",
                          "hy", "id", "ig", "is", "it", "iw", "ja", "jv", "ka",
                          "kk", "km", "kn", "ko", "kri", "ku", "ky", "la", "lb",
                          "lg", "ln", "lo", "lt", "lv", "mg", "mi", "mk", "ml",
                          "mn", "mr", "ms", "mt", "my", "ne", "nl", "no", "nso",
                          "ny", "om", "or", "pa", "pl", "ps", "pt", "qu", "ro",
                          "ru", "rw", "sa", "sd", "si", "sk", "sl", "sm", "sn",
                          "so", "sq", "sr", "st", "su", "sv", "sw", "ta", "te",
                          "tg", "th", "ti", "tk", "tl", "tr", "ts", "tt", "ug",
                          "uk", "ur", "uz", "vi", "xh", "yi", "yo", "zu", "en-CA"]

    import re

    def extract_video_id(self, input):
        if input.startswith("/watch?v="):
            parsed_url = urlparse(input)
            query_params = parse_qs(parsed_url.query)
            video_id = query_params.get('v', [None])[0]
            return video_id
        if input.startswith("/shorts/"):
            video_id = input.split("/shorts/")[1]
            return video_id
        if re.match(r"^[a-zA-Z0-9_-]{11}$", input):
            return input
        return None

    def load_from_url(self, url: str = "https://lilianweng.github.io/posts/2023-06-23-agent/",
                      **kwargs) -> List[Document]:
        self.loader = WebBaseLoader(url, **kwargs)
        self.data = self.loader.load()
        return self.data

    def load_from_youtube(self, video_id: str = "Unzc731iCUY", 
                          query: list = None, num_videos: int = 2,
                          **kwargs) -> List[Document]:
        if query is not None:
            urls = []
            self.data = []
            tool = YouTubeSearchTool()
            for item in query:
                urls.extend(ast.literal_eval(tool.run(item + f" , {num_videos}")))
            urls = set(urls)
            print(len(urls))
            for url in urls:
                video_id = self.extract_video_id(url)
                loader = YoutubeLoader(language=self.languages, video_id=video_id)
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