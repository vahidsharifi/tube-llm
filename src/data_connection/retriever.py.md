# Retriever Class Documentation

[Linked Table of Contents](#table-of-contents)

## Table of Contents <a name="table-of-contents"></a>

* [1. Class Overview](#class-overview)
* [2. `__init__` Method](#init-method)
* [3. `get_similar_docs` Method](#get-similar-docs-method)
* [4. `get_multi_query` Method](#get-multi-query-method)


## 1. Class Overview <a name="class-overview"></a>

The `Retriever` class facilitates the retrieval of relevant documents from a vector store based on a given query.  It offers two primary methods: `get_similar_docs` for simple similarity search and `get_multi_query` for more sophisticated multi-query retrieval leveraging a large language model (LLM).


## 2. `__init__` Method <a name="init-method"></a>

```python
def __init__(self, vectore_store):
    self.vectore_store = vectore_store
    self.documents = None
```

This constructor initializes the `Retriever` object.

| Parameter | Description | Type |
|---|---|---|
| `vectore_store` |  An instance of a vector store (e.g., FAISS, ChromaDB) containing the indexed documents. | Object |


The `self.documents` attribute is initialized to `None`. It will store the retrieved documents after a query.


## 3. `get_similar_docs` Method <a name="get-similar-docs-method"></a>

```python
def get_similar_docs(self, question: str = "What are the approaches to Task Decomposition?"):
    self.documents = self.vectore_store.similarity_search(question)
    return self.documents
```

This method performs a simple similarity search using the underlying vector store.

| Parameter | Description | Type | Default Value |
|---|---|---|---|
| `question` | The query string. | `str` | "What are the approaches to Task Decomposition?" |

The method directly uses the `similarity_search` method provided by the `vectore_store` object.  The returned documents are stored in `self.documents` and also returned by the function.  The algorithm used for similarity search is determined by the underlying vector store implementation (e.g., cosine similarity, dot product).


## 4. `get_multi_query` Method <a name="get-multi-query-method"></a>

```python
def get_multi_query(self, question):
    llm = ChatOpenAI(temperature=0)
    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever=self.vectore_store.as_retriever(), llm=llm
    )
    self.documents = retriever_from_llm.get_relevant_documents(query=question)
    return self.documents
```

This method utilizes the `langchain` library's `MultiQueryRetriever` to perform a more advanced retrieval process.

| Parameter | Description | Type |
|---|---|---|
| `question` | The query string. | `str` |

This method leverages a large language model (LLM) to generate multiple queries based on the input `question`.  The algorithm works as follows:

1. **LLM Initialization:** A `ChatOpenAI` LLM is initialized with a temperature of 0, ensuring deterministic output.
2. **Multi-Query Retriever Creation:** A `MultiQueryRetriever` is created using the vector store's retriever and the initialized LLM.  This retriever uses the LLM to expand the initial query into multiple related queries.
3. **Retrieval:** The `get_relevant_documents` method of the `MultiQueryRetriever` is called, using the expanded queries to search the vector store.  This returns a combined set of documents relevant to all generated queries.
4. **Result Storage and Return:** The retrieved documents are stored in `self.documents` and returned.

The underlying algorithm of `MultiQueryRetriever` involves prompting the LLM to reformulate the initial query into multiple variations, effectively broadening the search scope and improving recall.  The specific prompting strategy is defined within the `MultiQueryRetriever` implementation.
