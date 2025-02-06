# Internal Code Documentation: Data Loader Class

## Table of Contents

* [1. Introduction](#1-introduction)
* [2. Class `Loader`](#2-class-loader)
    * [2.1 `__init__` Method](#21-__init__-method)
    * [2.2 `extract_video_id` Method](#22-extract_video_id-method)
    * [2.3 `load_from_url` Method](#23-load_from_url-method)
    * [2.4 `load_from_youtube` Method](#24-load_from_youtube-method)
    * [2.5 `load_from_arxiv` Method](#25-load_from_arxiv-method)
    * [2.6 `load_from_wikipedia` Method](#26-load_from_wikipedia-method)


## 1. Introduction

This document provides internal code documentation for the `Loader` class. This class utilizes the `langchain` library to load data from various sources, including web pages, YouTube videos, arXiv papers, and Wikipedia articles.  It provides methods for loading data from each source, handling potential errors gracefully.


## 2. Class `Loader`

This class encapsulates the functionality to load documents from different sources.

### 2.1 `__init__` Method

```python
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
```

The constructor initializes the `Loader` object. It sets the `loader` attribute to `None` (to be populated later by specific loaders), `data` to `None` (to store loaded data), and defines a list `languages` containing various language codes used for YouTube video loading.


### 2.2 `extract_video_id` Method

```python
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
```

This method extracts the YouTube video ID from different input formats. It checks if the input starts with "/watch?v=", "/shorts/", or matches a regular expression for a standard 11-character video ID.  It returns the video ID if found, otherwise `None`.

### 2.3 `load_from_url` Method

```python
    def load_from_url(self, urls: list = ["https://lilianweng.github.io/posts/2023-06-23-agent/"],
                      **kwargs) -> List[Document]:
        self.data = []
        for url in urls:
            try:
                self.loader = WebBaseLoader(url, **kwargs)
                self.data.extend(self.loader.load())
            except:
                continue
        return self.data
```

This method loads data from a list of URLs using `WebBaseLoader`. It iterates through each URL, creates a `WebBaseLoader` instance, loads the data using `loader.load()`, and extends the `self.data` list.  A `try-except` block handles potential exceptions during loading.


### 2.4 `load_from_youtube` Method

```python
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
```

This method loads data from YouTube.  If a `query` list is provided, it uses `YouTubeSearchTool` to get video URLs, then extracts video IDs and loads data using `YoutubeLoader`. Otherwise, it loads data using a single `video_id`.  The `ast.literal_eval` safely evaluates the string output of the `YouTubeSearchTool`.


### 2.5 `load_from_arxiv` Method

```python
    def load_from_arxiv(self, query: str,
                        **kwargs) -> List[Document]:
        self.loader = ArxivLoader(query=query, **kwargs)
        self.data = self.loader.load()
        return self.data
```

This method loads data from arXiv using `ArxivLoader` based on the provided `query`.


### 2.6 `load_from_wikipedia` Method

```python
    def load_from_wikipedia(self, query: str,
                            **kwargs) -> List[Document]:
        self.loader = WikipediaLoader(query=query, **kwargs)
        self.data = self.loader.load()
        return self.data
```

This method loads data from Wikipedia using `WikipediaLoader` based on the provided `query`.

