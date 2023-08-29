import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.routers.answer_router import router as answer_router
from fastapi.templating import Jinja2Templates

app = FastAPI(debug=True)

# Configure CORS to allow requests from the frontend (replace * with your frontend URL)
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

# Define the project root and mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")
app.include_router(answer_router, prefix="/answer", tags=["Answer"])


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

    # INDEX_PATH = "index.html"
    # with open(INDEX_PATH) as f:
    #     return f.read()
