# Internal Code Documentation: Chain Class

## Table of Contents

* [1. Introduction](#1-introduction)
* [2. Class `Chain`](#2-class-chain)
    * [2.1 `__init__` Method](#21-__init__-method)
    * [2.2 `input_query_modifier` Method](#22-input_query_modifier-method)
    * [2.3 `input_query_modifier_multi` Method](#23-input_query_modifier_multi-method)
    * [2.4 `youtube_summarizer` Method](#24-youtube_summarizer-method)


## 1. Introduction

This document provides internal code documentation for the `Chain` class, outlining its functionality and the algorithms employed within its methods.  The class leverages the Langchain library for interaction with large language models (LLMs) and performs tasks related to query modification and YouTube video summarization.

## 2. Class `Chain`

The `Chain` class encapsulates methods for modifying user queries to optimize YouTube searches and summarizing content from YouTube videos.

### 2.1 `__init__` Method

```python
def __init__(self):
    self.llm = None
    self.prompt = None
```

This constructor initializes the `Chain` object. It sets the `llm` and `prompt` attributes to `None`. These attributes will be populated later by the other methods within the class as needed.


### 2.2 `input_query_modifier` Method

```python
def input_query_modifier(self, query: str = "How to fine-tune an llm with limited resources?",
                         **kwargs) -> str:
    # ... (Prompt templates) ...

    self.prompt = ChatPromptTemplate.from_template(template_2)
    self.llm = ChatOpenAI(temperature=0.0)
    chain = LLMChain(llm=self.llm, prompt=self.prompt)
    return [chain.run(query).replace(",", " ")] #Replacing the comma with spaces due to YouTubeSearchTool documentation
```

This method modifies a given user query to improve its effectiveness for YouTube searches.

* **Algorithm:** The method uses a zero-shot prompt (template_2) to instruct the LLM to generate a modified query.  The prompt instructs the LLM to create a concise and effective equivalent query for YouTube search.  The LLM's response is then processed by replacing commas with spaces to ensure compatibility with the `YouTubeSearchTool` (as noted in the inline comment). The `ChatOpenAI` model is used with `temperature=0.0` to ensure deterministic outputs.  The Langchain's `LLMChain` facilitates the interaction with the LLM.


### 2.3 `input_query_modifier_multi` Method

```python
def input_query_modifier_multi(self, query: str = "How to fine-tune an llm with limited resources?",
                              **kwargs) -> dict:
    # ... (Prompt templates) ...

    self.prompt = ChatPromptTemplate.from_template(template_1)
    self.llm = ChatOpenAI(temperature=0.0)
    chain = LLMChain(llm=self.llm, prompt=self.prompt)
    queries = chain.run(query)
    queries = ast.literal_eval(queries)
    queries = [item.replace(",", " ") for item in queries.values()]
    return queries
```

This method generates multiple modified queries from a single input query.

* **Algorithm:** Similar to `input_query_modifier`, this method utilizes an LLM (this time using template_1) to generate multiple query variations.  The crucial difference is that the prompt instructs the LLM to return the modified queries in JSON format. The response is parsed using `ast.literal_eval` to convert the JSON string into a Python dictionary.  Then, commas are removed from each generated query before returning a list of these modified queries.


### 2.4 `youtube_summarizer` Method

```python
def youtube_summarizer(self, urls):
    self.llm = ChatOpenAI(temperature=0.0)
    summaries = []
    split = Transformer()
    loader = Loader()
    for url in urls:
        video_id = url.replace("https://www.youtube.com/watch?v=", "", 1)
        data = loader.load_from_youtube(video_id=video_id)
        docs = split.split_data(data)
        chain = load_summarize_chain(llm=self.llm, chain_type='refine')
        summary = chain.run(docs)
        summaries.append(summary)
    return summaries
```

This method summarizes multiple YouTube videos.

* **Algorithm:** The method iterates through a list of YouTube video URLs. For each URL, it extracts the video ID, retrieves the video data using a `Loader` object (presumably a custom class handling data retrieval), splits the data into smaller chunks using a `Transformer` object (another custom class likely for text splitting), and then uses Langchain's `load_summarize_chain` with a 'refine' chain type to generate a summary of the video.  The summaries of all videos are collected and returned as a list.  The `ChatOpenAI` LLM is again used with `temperature=0.0` for deterministic summaries.  This implies the `Loader` and `Transformer` classes handle the complexities of YouTube data retrieval and text processing, respectively.
