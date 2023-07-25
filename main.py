"""
It takes input of a link and answers any question.
"""
from src import Loader, Transformer, Store, Retriever
from src import QuestionAnswering

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    LINK = "https://docs.subconscious.ai/"
    VIDEO_ID = "Unzc731iCUY"
    QUERY = "research trends on large language models"
    QUESTION = "What are the research trends in LLMs?"

    # Load, Transform, Store, Retrieve
    loader = Loader()
    # data = loader.load_from_url(url=LINK)
    # data = loader.load_from_youtube(video_id=VIDEO_ID)
    data = loader.load_from_youtube(query=QUESTION)
    # data = loader.load_from_arxiv(query=QUERY, load_max_docs=5)
    # data = loader.load_from_wikipedia(query=QUERY, load_max_docs=5)
    print(f"{len(data)} DOCUMENTS LOADED")
    # print(data)
    # print(data)

    split = Transformer()
    data_splits = split.split_data(data)
    # print(data_splits)

    store = Store()
    vectore_store = store.store_data(splits=data_splits)
    # print(vectore_store)

    # Retrieval
    ret = Retriever(vectore_store=vectore_store)
    documents = ret.get_similar_docs(question=QUESTION)
    # print(documents)

    # Question Answering
    qa = QuestionAnswering(vector_store=vectore_store)
    answer_results = qa.ask(question=QUESTION)
    print(answer_results['result'])
    # print(answer_results)


    # # Printing source videos for youtube search engine
    # print(*set("https://www.youtube.com/watch?v=" + source.metadata['source'] for source in answer_results['source_documents']), sep='\n')
