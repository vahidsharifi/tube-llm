"""
It takes input of a link and answers any question.
"""
from src import Loader, Split, Store
from src import Retrieval, QuestionAnswering

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    LINK = "https://docs.subconscious.ai/"
    QUESTION = "How subconscious.ai works ?"

    # Load, Split, Store
    loader = Loader()
    data = loader.load_from_url(url=LINK)
    # print(data)

    split = Split()
    data_splits = split.split_data(data)
    # print(data_splits)

    store = Store()
    vectore_store = store.store_data(splits=data_splits)
    # print(vectore_store)

    # Retrieval
    ret = Retrieval(vectore_store=vectore_store)
    documents = ret.get_similar_docs(question=QUESTION)
    # print(documents)

    # Question Answering
    qa = QuestionAnswering(vector_store=vectore_store)
    answer_results = qa.ask(question=QUESTION)
    print(answer_results['result'])
