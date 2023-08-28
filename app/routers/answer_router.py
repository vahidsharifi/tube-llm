from fastapi import APIRouter, Query
from src import Loader, Transformer, Store, Retriever, Chain, Tools, QuestionAnswering
from app.models.input_models import QuestionInput
from app.models.output_models import ResponseModel
from app.utils.enums import PerformanceTypes, SearchTypes
import pandas as pd
import wandb
import datetime

router = APIRouter()

run = wandb.init(project="tube-llm", entity="vahidsharifi")

@router.get("/", response_model=ResponseModel)
async def answer_question(
        question: str = Query(...),
        performance: PerformanceTypes = Query(PerformanceTypes.fast),
        searchType: SearchTypes = Query(SearchTypes.youtube)
) -> ResponseModel:
    chain = Chain()
    loader = Loader()
    split = Transformer()
    store = Store()

    # Default values for the response model
    default_response = {
        "question": None,
        "modified_question": None,
        "answer": None,
        "sources": None
    }

    if searchType == SearchTypes.youtube:

        qa = QuestionAnswering()

        if performance == PerformanceTypes.basic:
            QUESTION = [question.replace(',', ' ')]
            data = loader.load_from_youtube(query=QUESTION)

        elif performance == PerformanceTypes.fast:
            QUESTION = chain.input_query_modifier(question)
            data = loader.load_from_youtube(query=QUESTION)

        elif performance == PerformanceTypes.normal:
            QUESTION = chain.input_query_modifier_multi(question)
            data = loader.load_from_youtube(query=QUESTION)

        else:  # assuming this is for PerformanceTypes.advanced or any other condition
            QUESTION = chain.input_query_modifier_multi(question)
            data = loader.load_from_youtube(query=QUESTION)

        data_splits = split.split_data(data)
        vectore_store = store.store_data(splits=data_splits)

        if performance in [PerformanceTypes.basic, PerformanceTypes.fast, PerformanceTypes.normal]:
            answer_results = qa.ask(question=question, vector_store=vectore_store)
            default_response.update({
                "question": question,
                "modified_question": QUESTION,
                "answer": [answer_results['result']],
                "sources": [list(set("https://www.youtube.com/watch?v=" + source.metadata['source'] for source in
                                     answer_results['source_documents']))]
            })

        else:  # for advanced or any other condition
            ret = Retriever(vectore_store=vectore_store)
            documents = ret.get_multi_query(question=QUESTION)
            answer_results, sources = qa.ask_multi_query(documents=documents, question=question)
            default_response.update({
                "question": question,
                "modified_question": QUESTION,
                "answer": [answer_results['output_text']],
                "sources": sources
            })
        
        df = pd.DataFrame(default_response)
        my_table = wandb.Table(dataframe=df)
        run.log({f"{datetime.datetime.now()}": my_table})

    return ResponseModel(**default_response)

    # chain = Chain()
    #     summaries = chain.youtube_summarizer(response["sources"][0])
    #     print(summaries)

        

    # Add more conditions for "normal", "advanced", and "web" here as per your requirement
