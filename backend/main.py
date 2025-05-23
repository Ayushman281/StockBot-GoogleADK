import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from agents.orchestrator import StockOrchestratorAgent

# Load environment variables
load_dotenv()

app = FastAPI(title="StockBot API", description="Multi-agent stock analysis system")

# Get frontend URL from environment or use a default list
frontend_url = os.environ.get("FRONTEND_URL", "https://your-vercel-app-url.vercel.app")
allowed_origins = [frontend_url]

# For development, also allow localhost origins
if os.environ.get("ENVIRONMENT") != "production":
    allowed_origins.extend(["http://localhost:5173", "http://localhost:3000"])

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Accepts requests from deployed frontend and local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    text: str

class Response(BaseModel):
    answer: str
    metadata: dict = {}

# Initialize the orchestrator agent
orchestrator = StockOrchestratorAgent()

@app.post("/query", response_model=Response)
async def process_query(query: Query):
    try:
        result = orchestrator.process_query(query.text)
        return Response(answer=result["answer"], metadata=result["metadata"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
