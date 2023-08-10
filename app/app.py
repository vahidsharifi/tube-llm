import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.routers.answer_router import router as answer_router

app = FastAPI(debug=True)

# Configure CORS to allow requests from the frontend (replace * with your frontend URL)
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

# Define the project root and mount the static files directory
PROJECT_ROOT = Path(__file__).parent.parent
app.mount("/static", StaticFiles(directory=PROJECT_ROOT / "static"), name="static")

app.include_router(answer_router, prefix="/answer", tags=["Answer"])

@app.get("/", response_class=HTMLResponse)
async def read_index():
    INDEX_PATH = PROJECT_ROOT / "static" / "index.html"
    with open(INDEX_PATH) as f:
        return f.read()
