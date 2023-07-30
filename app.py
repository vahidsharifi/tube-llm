from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import List
import wandb
import datetime

# Import your existing classes and functions here
from src import Loader, Transformer, Store, Retriever
from src import QuestionAnswering

run = wandb.init(project="tube-llm", entity="vahidsharifi")

# Create an instance of the FastAPI app
app = FastAPI()

# Configure CORS to allow requests from the frontend (replace * with your frontend URL)
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

# Define a route to serve the index.html file
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html") as f:
        return f.read()

# Wrap your existing code into a FastAPI route
@app.get("/answer/")
async def answer_question(question: str):
    # Your existing code starts here
    QUESTION = question

    # Load, Transform, Store, Retrieve
    loader = Loader()
    data = loader.load_from_youtube(query=QUESTION)
    print(f"{len(data)} DOCUMENTS LOADED")

    split = Transformer()
    data_splits = split.split_data(data)

    store = Store()
    vectore_store = store.store_data(splits=data_splits)

    # Retrieval
    ret = Retriever(vectore_store=vectore_store)
    documents = ret.get_similar_docs(question=QUESTION)

    # Youtube Question Answering
    qa = QuestionAnswering(vector_store=vectore_store)
    answer_results = qa.ask(question=QUESTION)
    # Your existing code ends here

    # Return the results as JSON
    response = {
        "question": [QUESTION],
        "answer": [answer_results['result']],
        "sources": [", ".join(list(set("https://www.youtube.com/watch?v=" + source.metadata['source'] for source in answer_results['source_documents'])))]
    }
    import pandas as pd
    df = pd.DataFrame(response)
    # print("Response: ", response)
    # Log the results
    # wandb.log({'my_dic':response})
    my_table = wandb.Table(dataframe=df)
    run.log({f"{datetime.datetime.now()}": my_table})

    return response
