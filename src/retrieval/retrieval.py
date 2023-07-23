class Retrieval:
    def __init__(self, vectore_store):
        self.vectore_store = vectore_store

    def get_similar_docs(self, question: str = "What are the approaches to Task Decomposition?"):
        self.documents = self.vectore_store.similarity_search(question)
        return self.documents
