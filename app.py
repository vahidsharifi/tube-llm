from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import wandb
import datetime
import pandas as pd


# Import your existing classes and functions here
from src import Loader, Transformer, Store, Retriever, Chain
from src import QuestionAnswering

run = wandb.init(project="tube-llm", entity="vahidsharifi")

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
    with open("static/index.html") as f:
        return f.read()

# Wrap your existing code into a FastAPI route
@app.get("/answer/")
async def answer_question(question: str):

    print("Received query:", question)
    chain = Chain()
    QUESTION = chain.input_query_modifier(question)
    print("modified query:", QUESTION)

    # Load, Transform, Store, Retrieve
    loader = Loader()
    data = loader.load_from_youtube(query=QUESTION)
    print(f"{len(data)} DOCUMENTS LOADED")

    split = Transformer()
    data_splits = split.split_data(data)

    store = Store()
    vectore_store = store.store_data(splits=data_splits)


    # # Youtube Question Answering Multi Query Retriever
    # # Retriever
    # ret = Retriever(vectore_store=vectore_store)
    # documents = ret.get_multi_query(question=QUESTION)
    # qa = QuestionAnswering()
    # answer_results, sources = qa.ask_multi_query(documents=documents, question=question)
    # # Return the results as JSON
    # response = {
    #     "question": [question],
    #     "modified_question": [QUESTION],
    #     "answer": [answer_results['output_text']],
    #     "sources": sources
    # }


    # Youtube Question Answering Simple Retriever
    qa = QuestionAnswering()
    answer_results = qa.ask(question=question, vector_store=vectore_store)
    # Your existing code ends here

    # Return the results as JSON
    response = {
        "question": [question],
        "modified_question": [QUESTION],
        "answer": [answer_results['result']],
        "sources": [list(set("https://www.youtube.com/watch?v=" + source.metadata['source'] for source in answer_results['source_documents']))]
    }
    



    df = pd.DataFrame(response)
    my_table = wandb.Table(dataframe=df)
    run.log({f"{datetime.datetime.now()}": my_table})

    return response
