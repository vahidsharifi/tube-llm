from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate 
from langchain.chains.question_answering import load_qa_chain


template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.\
Use six sentences maximum and keep the answer as concise as possible. 

Context:{context}

Question: {question}

Helpful Answer:"""

QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template, )


class QuestionAnswering:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        self.vector_store = None

    def ask(self, question, vector_store):
        self.vector_store = vector_store
        qa_chain = RetrievalQA.from_chain_type(self.llm,
                                               retriever=self.vector_store.as_retriever(),
                                               chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
                                               return_source_documents=True)
        return qa_chain({"query": question})
    
    def ask_multi_query(self, question, documents):
        chain = load_qa_chain(self.llm, chain_type="stuff")
        sources = [list(set("https://www.youtube.com/watch?v=" + document.metadata['source'] for document in documents))]
        answer = chain({"input_documents": documents, "question": question},return_only_outputs=True)
        return answer, sources
    