from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sys
sys.path.insert(0, ".")
from src.pipeline import get_recommendations

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

@app.post("/recommend")
def recommend(body: Query):
    standards, latency = get_recommendations(body.query)
    return {
        "standards": standards,
        "latency": latency
    }

app.mount("/", StaticFiles(directory="static", html=True), name="static")