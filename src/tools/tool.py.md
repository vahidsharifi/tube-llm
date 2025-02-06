# Internal Documentation: Tools Class

[Linked Table of Contents](#linked-table-of-contents)

## Linked Table of Contents

* [1. Introduction](#1-introduction)
* [2. Class Overview: `Tools`](#2-class-overview-tools)
    * [2.1 Constructor: `__init__`](#21-constructor-__init__)
    * [2.2 Method: `duckduckgo_search`](#22-method-duckduckgo_search)


## 1. Introduction

This document provides internal documentation for the `Tools` class, which utilizes the `langchain` library to interact with external search engines.  Specifically, it demonstrates the use of DuckDuckGo for search queries.


## 2. Class Overview: `Tools`

The `Tools` class encapsulates methods for interacting with various external tools. Currently, it only includes a method for performing DuckDuckGo searches.

### 2.1 Constructor: `__init__`

```python
def __init__(self):
    pass
```

The constructor (`__init__`) for the `Tools` class is currently empty.  No initialization is required at object creation.


### 2.2 Method: `duckduckgo_search`

```python
def duckduckgo_search(self, query: str = "How to fine-tune LLamA-2?", num_results: int = 4, **kwargs):
    search = DuckDuckGoSearchResults(num_results=num_results)
    result = search.run(query)
    return result
```

This method utilizes the `DuckDuckGoSearchResults` tool from the `langchain` library to perform a DuckDuckGo search.

**Algorithm:**

1. **Initialization:** A `DuckDuckGoSearchResults` object is created. The `num_results` parameter specifies the desired number of search results to retrieve (defaults to 4).  Additional keyword arguments (`**kwargs`) can be passed to the `DuckDuckGoSearchResults` constructor for further customization (though none are used in this example).

2. **Search Execution:** The `run()` method of the `DuckDuckGoSearchResults` object is called with the provided `query` string. This method sends the query to DuckDuckGo, retrieves the results, and formats them.

3. **Result Return:** The formatted search results, as returned by `search.run()`, are returned by the `duckduckgo_search` method.  The exact format of the returned results is determined by the `langchain` library's `DuckDuckGoSearchResults` implementation.  It typically involves a structured representation of the search results, likely including titles, URLs, and snippets.


**Parameters:**

| Parameter      | Type     | Description                                                              | Default Value            |
|-----------------|----------|--------------------------------------------------------------------------|--------------------------|
| `query`        | `str`    | The search query to submit to DuckDuckGo.                               | "How to fine-tune LLamA-2?" |
| `num_results` | `int`    | The number of search results to retrieve.                               | 4                        |
| `**kwargs`     | `dict`   | Additional keyword arguments passed to the `DuckDuckGoSearchResults` constructor. |  {}                       |

**Return Value:**

The method returns the results of the DuckDuckGo search as processed by the `langchain` library.  The specific data structure of this return value is defined by the `langchain` library and is not explicitly specified here but would need to be referenced in `langchain`'s documentation.


**Example Usage:**

```python
results = Tools().duckduckgo_search(query="What is Langchain?", num_results=2)
print(results)
```
