from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chat_models import ChatOpenAI

class Retriever:
    def __init__(self, vectore_store):
        self.vectore_store = vectore_store
        self.documents = None

    def get_similar_docs(self, question: str = "What are the approaches to Task Decomposition?"):
        self.documents = self.vectore_store.similarity_search(question)
        return self.documents

    def get_multi_query(self, question):
        llm = ChatOpenAI(temperature=0)
        retriever_from_llm = MultiQueryRetriever.from_llm(
            retriever=self.vectore_store.as_retriever(), llm=llm
            )
        self.documents = retriever_from_llm.get_relevant_documents(query=question)   
        return self.documents

    
