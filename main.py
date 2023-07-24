"""
It takes input of a link and answers any question.
"""
from src import Loader, Split, Store
from src import Retrieval, QuestionAnswering

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    LINK = "https://docs.subconscious.ai/"
    VIDEO_ID = "Unzc731iCUY"
    QUERY = "research trends on large language models"
    QUESTION = "What are the research trends in LLMs?"

    # Load, Split, Store
    loader = Loader()

    # Load a web page
    # data = loader.load_from_url(url=LINK)
    # data = loader.load_from_youtube(video_id=VIDEO_ID)
    data = loader.load_from_youtube(query=QUESTION)
    # data = loader.load_from_arxiv(query=QUERY, load_max_docs=5)
    # data = loader.load_from_wikipedia(query=QUERY, load_max_docs=5)
    print(f"{len(data)} DOCUMENTS LOADED")
    # print(data)
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
