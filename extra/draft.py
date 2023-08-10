import enum
# 3.5/10
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import wandb
import datetime
import pandas as pd

# Import your existing classes and functions here
from src import Loader, Transformer, Store, Retriever, Chain, Tools
from src import QuestionAnswering

# run = wandb.init(project="tube-llm", entity="vahidsharifi")

# Create an instance of the FastAPI app
app = FastAPI()

# Configure CORS to allow requests from the frontend (replace * with your frontend URL)
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


# Define a route to serve the index.html file
@app.get("/", response_class=HTMLResponse)
async def read_index():
    # Load using jinja2 templates
    with open("../static/index.html") as f:
        return f.read()


#  Wrap your existing code into a FastAPI route -- WTF is this ?
@app.get("/answer/")
async def answer_question(question: str, performance: str = "fast", searchType: str = "youtube"):
    """

    Use data models for creating input fields and specifying types
    Use enums for defining consatants
    Use proper functions
    Organise in your guide in proper files

    :param question:
    :param performance:
    :param searchType:
    :return:
    """
    print("Received query:", question)
    # Make an infercae class or something which auto does this init
    # It's not recommend to include this much code in an api. Ideally we expect only interface
    chain = Chain()
    loader = Loader()
    split = Transformer()
    store = Store()

    if searchType == "youtube":
        if performance == "basic":  # Original Query - Simple Retriever - Simple Search Query
            QUESTION = question.replace(',', ' ')
            data = loader.load_from_youtube(query=[QUESTION])
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

        elif performance == "fast":  # Modified Query - Simple Retriever - Simple Search Query
            QUESTION = chain.input_query_modifier(question)  # Single query search in youtube
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
                                     answer_results['source_documents']))]}

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

        # define proper response schema and use those.
        return response


    elif searchType == "web":
        tool = Tools()
        # Code for handling web search
        # search = tool.duckduckgo_search(question, num_results=2)
        # # search
        # # print(search)
        # urls = [item['link'] for item in search]
        # data = loader.load_from_url(urls=urls)
        # data_splits = split.split_data(data)
        # # print(data_splits[10])
        # vectore_store = store.store_data(splits=data_splits)
        # qa = QuestionAnswering()
        # answer_results = qa.ask(question=question, vector_store=vectore_store)
        # response = {
        #     "question": [question],
        #     "modified_question": [question],
        #     "answer": [answer_results['result']],
        #     "sources": [list(set(source.metadata['source'] for source in
        #                          answer_results['source_documents']))]
        # }
        #
        # print(response['answer'])
        # print(answer_results['source_documents'])

        QUESTION = chain.input_query_modifier(question)  # Multi query search in youtube
        search = tool.duckduckgo_search(QUESTION[0], num_results=4)
        print("modified query:", QUESTION)
        print(search)
        # urls = [item['link'] for item in search]
        # print(urls)
        # data = loader.load_from_url(urls=urls)
        # print(f"{len(data)} DOCUMENTS LOADED")
        # data_splits = split.split_data(data)
        # print(data_splits)
        # vectore_store = store.store_data(splits=data_splits)
        # ret = Retriever(vectore_store=vectore_store)
        # documents = ret.get_multi_query(question=QUESTION)
        # qa = QuestionAnswering()
        # answer_results, sources = qa.ask_multi_query(documents=documents, question=question)
        # response = {
        #     "question": [question],
        #     "modified_question": [QUESTION],
        #     "answer": [answer_results['output_text']],
        #     "sources": sources
        # }
        #
        # print(response['answer'])
        # # print(answer_results['source_documents'])
