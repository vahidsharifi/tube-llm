from fastapi import APIRouter, Body, Query
from src import Loader, Transformer, Store, Retriever, Chain, Tools
from src import QuestionAnswering
from app.models.input_models import QuestionInput
from app.models.output_models import ResponseModel
from app.utils.enums import PerformanceTypes, SearchTypes
import pandas as pd

router = APIRouter()

# run = wandb.init(project="tube-llm", entity="vahidsharifi")


@router.get("/", response_model=ResponseModel)
async def answer_question(
    question: str = Query(...),
    performance: PerformanceTypes = Query(PerformanceTypes.fast),
    searchType: SearchTypes = Query(SearchTypes.youtube)
):
    chain = Chain()
    loader = Loader()
    split = Transformer()
    store = Store()

    if searchType == "youtube":
        if performance == "basic":  # Original Query - Simple Retriever - Simple Search Query
            QUESTION = question.replace(',', ' ')
            data = loader.load_from_youtube(query=[QUESTION])
            data_splits = split.split_data(data)
            vectore_store = store.store_data(splits=data_splits)
            qa = QuestionAnswering()
            answer_results = qa.ask(question=question, vector_store=vectore_store)
            response = {
                "question": question,
                "modified_question": QUESTION,
                "answer": [answer_results['result']],
                "sources": [list(set("https://www.youtube.com/watch?v=" + source.metadata['source'] for source in
                                     answer_results['source_documents']))]
            }
            return response

        elif performance == "fast":  # Modified Query - Simple Retriever - Simple Search Query
            QUESTION = chain.input_query_modifier(question)  # Single query search in youtube
            data = loader.load_from_youtube(query=QUESTION)
            data_splits = split.split_data(data)
            vectore_store = store.store_data(splits=data_splits)
            qa = QuestionAnswering()
            answer_results = qa.ask(question=question, vector_store=vectore_store)
            response = {
                "question": question,
                "modified_question": QUESTION,
                "answer": [answer_results['result']],
                "sources": [list(set("https://www.youtube.com/watch?v=" + source.metadata['source'] for source in
                                     answer_results['source_documents']))]
            }
            return response

        elif performance == "normal":  # Modified Query - Simple Retriever - Multiple Search Query
            QUESTION = chain.input_query_modifier_multi(question)  # Multi query search in youtube
            print("modified query:", QUESTION)
            data = loader.load_from_youtube(query=QUESTION)
            data_splits = split.split_data(data)
            print(f"{len(data)} DOCUMENTS LOADED")
            vectore_store = store.store_data(splits=data_splits)
            qa = QuestionAnswering()
            answer_results = qa.ask(question=question, vector_store=vectore_store)
            response = {
                "question": [question],
                "modified_question": [QUESTION],
                "answer": [answer_results['result']],
                "sources": [list(set("https://www.youtube.com/watch?v=" + source.metadata['source'] for source in
                                     answer_results['source_documents']))]
            }
            return response

        else:  # Modified Query - Multiple Retriever - Multiple Search Query
            QUESTION = chain.input_query_modifier_multi(question)  # Multi query search in youtube
            print("modified query:", QUESTION)
            data = loader.load_from_youtube(query=QUESTION)
            print(f"{len(data)} DOCUMENTS LOADED")
            data_splits = split.split_data(data)
            vectore_store = store.store_data(splits=data_splits)
            ret = Retriever(vectore_store=vectore_store)
            documents = ret.get_multi_query(question=QUESTION)
            qa = QuestionAnswering()
            answer_results, sources = qa.ask_multi_query(documents=documents, question=question)
            response = {
                "question": [question],
                "modified_question": [QUESTION],
                "answer": [answer_results['output_text']],
                "sources": sources
            }

        # chain = Chain()
        # summaries = chain.youtube_summarizer(response["sources"][0])
        # print(summaries)

        # df = pd.DataFrame(response)
        # my_table = wandb.Table(dataframe=df)
        # run.log({f"{datetime.datetime.now()}": my_table})

    # Add more conditions for "normal", "advanced", and "web" here as per your requirement
