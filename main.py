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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define the project root and mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")
app.include_router(answer_router, prefix="", tags=["Answer"])

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Add this block to ensure the app listens on the port provided by the environment variable
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))  # Get the PORT from the environment, default to 8080
    uvicorn.run(app, host="0.0.0.0", port=port)
