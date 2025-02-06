# Question Answering System Documentation

[Linked Table of Contents](#linked-table-of-contents)


## Linked Table of Contents

* [1. Introduction](#1-introduction)
* [2. Class `QuestionAnswering`](#2-class-questionanswering)
    * [2.1 `__init__` method](#21-__init__-method)
    * [2.2 `ask` method](#22-ask-method)
    * [2.3 `ask_multi_query` method](#23-ask-multi-query-method)
* [3. Prompt Template](#3-prompt-template)


## 1. Introduction

This document details the implementation of a question answering system using Langchain.  The system leverages a large language model (LLM) to answer questions based on provided context.  It offers two main functionalities: answering single questions based on a vector store and answering questions based on multiple provided documents.


## 2. Class `QuestionAnswering`

This class encapsulates the core logic for question answering.

### 2.1 `__init__` method

```python
def __init__(self):
    self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    self.vector_store = None
```

The constructor initializes the question answering object.

*   It sets up the LLM using `ChatOpenAI` with the `gpt-3.5-turbo` model and a temperature of 0 for deterministic outputs.
*   `self.vector_store` is initialized to `None`. It will store the vector database used for retrieval in the `ask` method.


### 2.2 `ask` method

```python
def ask(self, question, vector_store):
    self.vector_store = vector_store
    qa_chain = RetrievalQA.from_chain_type(self.llm,
                                           retriever=self.vector_store.as_retriever(),
                                           chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
                                           return_source_documents=True)
    return qa_chain({"query": question})
```

This method answers a question using a vector store for context retrieval.

*   The input `vector_store` is assigned to `self.vector_store`.
*   `RetrievalQA.from_chain_type` creates a retrieval QA chain.  This chain uses the specified LLM (`self.llm`), retrieves relevant documents from the vector store using `self.vector_store.as_retriever()`, and employs the custom prompt template (`QA_CHAIN_PROMPT`). `return_source_documents=True` ensures that the retrieved documents are included in the output.
*   The chain is then called with the input question (`{"query": question}`) to generate an answer.  The answer, along with the source documents, is returned.


### 2.3 `ask_multi_query` method

```python
def ask_multi_query(self, question, documents):
    chain = load_qa_chain(self.llm, chain_type="stuff")
    sources = [list(set("https://www.youtube.com/watch?v=" + document.metadata['source'] for document in documents))]
    answer = chain({"input_documents": documents, "question": question},return_only_outputs=True)
    return answer, sources
```

This method answers a question given a list of documents.

*   `load_qa_chain(self.llm, chain_type="stuff")` creates a QA chain using the "stuff" chain type. This type simply concatenates all input documents and passes them to the LLM along with the question.
*   The code extracts YouTube video IDs from the metadata of input documents and creates a list of URLs. Note that this assumes each document has a `source` key in its metadata containing a YouTube video ID.
*   The chain is executed with the documents and the question.  `return_only_outputs=True` ensures only the answer is returned.
*   The method returns the answer and the list of extracted YouTube URLs.


## 3. Prompt Template

```python
template = """Use the following pieces of context to answer the question at the end. 
Use six sentences maximum and keep the answer as concise as possible. Please note that
the language of question and Helpful Answer should be the same.

Please note that if you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:{context}

Question: {question}

Helpful Answer:"""

QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template, )
```

This section defines a prompt template used in the `ask` method.  The template instructs the LLM to answer the question concisely using the provided context and to explicitly state if it doesn't know the answer.  The `PromptTemplate` object is then created using this template, making it easily reusable.  The template ensures consistency in the LLM's response format.
