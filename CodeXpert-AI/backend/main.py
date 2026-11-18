
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analyzer import analyze_code

app = FastAPI(title="CodeXpert AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    language: str
    code: str

@app.get("/")
def home():
    return {"message": "CodeXpert AI Backend is running!"}

@app.post("/analyze")
def analyze(request: CodeRequest):
    return analyze_code(request.language, request.code)
