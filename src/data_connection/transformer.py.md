# Internal Code Documentation: Text Data Transformer

[Linked Table of Contents](#table-of-contents)

## Table of Contents

* [1. Overview](#1-overview)
* [2. Class `Transformer`](#2-class-transformer)
    * [2.1 Constructor `__init__`](#21-constructor-__init__)
    * [2.2 Method `split_data`](#22-method-split_data)
* [3. Main Execution Block](#3-main-execution-block)


## 1. Overview

This document details the functionality of the `Transformer` class, designed to split large text documents into smaller, manageable chunks using the `langchain` library.  The process leverages the `RecursiveCharacterTextSplitter` for efficient and contextually aware splitting.


## 2. Class `Transformer`

The `Transformer` class encapsulates the logic for splitting text data. It utilizes the `RecursiveCharacterTextSplitter` from the `langchain` library.

### 2.1 Constructor `__init__`

```python
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
```

The constructor initializes an instance of `RecursiveCharacterTextSplitter`.  This splitter divides text into chunks of approximately 1000 characters each, with a 50-character overlap between consecutive chunks. The overlap helps maintain context across chunk boundaries.

### 2.2 Method `split_data`

```python
    def split_data(self, data: List[Document]) -> List[Document]:
        all_splits = self.text_splitter.split_documents(data)
        return all_splits
```

The `split_data` method takes a list of `Document` objects as input (`data`).  It uses the pre-initialized `text_splitter` to divide these documents into smaller chunks.  The `split_documents` method from `langchain` handles the recursive splitting process, ensuring that the resulting chunks are within the specified size constraints while preserving sentence boundaries where possible. The function then returns a list of the newly created, smaller `Document` objects.

The algorithm behind `RecursiveCharacterTextSplitter` is a recursive approach. It attempts to split the input text at natural break points (like sentence endings). If a chunk exceeds the `chunk_size`, it recursively splits that chunk until all resulting chunks are within the size limit. The `chunk_overlap` ensures smooth transitions between chunks by including overlapping text.


## 3. Main Execution Block

```python
if __name__ == '__main__':
    from loader import Loader

    d = Loader().load_from_url()
    s = Split().split_data(d)
    print(s)
    print(type(s[0]))
```

The `if __name__ == '__main__':` block demonstrates the usage of the `Transformer` class. It imports a `Loader` class (presumably from a separate file), loads data from a URL using `Loader().load_from_url()`, and then uses an instance of `Split` (which seems to be a typo and should likely be `Transformer`) to split the loaded data. The resulting split data and the type of the first element in the result are printed to the console.  Note that the code implies the `Loader` class handles fetching and pre-processing of documents before passing them to the `Transformer`.  The exact implementation of `Loader` is not shown.
