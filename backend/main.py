from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import set_user_niche
import uvicorn

# Import the refactored agent functions and Pydantic models
from ScriptAgents import (
    get_topic_ideas,
    research_topic,
    generate_hook,
    generate_script,
)
from output_format import ResearchOutputList

# Initialize FastAPI app
app = FastAPI(
    title="AI ScriptWriter API",
    description="API for generating viral video scripts.",
    version="1.0.0",
)

# --- CORS Configuration ---
# This is crucial for allowing your React frontend to communicate with the backend.
origins = [
    "http://localhost:8001",  # Common for React dev server
    "http://localhost:5173",  # Common for Vite/React dev server
    "http://localhost:3000",  # Another common React port
    "http://127.0.0.1:5173",  # Vite local IP access
    "http://127.0.0.1:8001",  # Local IP access
    "http://127.0.0.1:3000",  # Local IP access
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
    expose_headers=["*"],
    max_age=600  # Cache preflight requests for 10 minutes
)

# --- Pydantic Models for Request Bodies ---
# These models provide data validation and documentation for your API.

class NicheRequest(BaseModel):
    niche: str

class TopicRequest(BaseModel):
    topic: str
    is_auto: bool = False

class HookRequest(BaseModel):
    research_report: str
    is_auto: bool = False

class ScriptRequest(BaseModel):
    hook: str
    research_report: str
    is_auto: bool = False

class TextResponse(BaseModel):
    content: str

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI ScriptWriter API"}

@app.post("/research/topics", response_model=TextResponse, summary="Get Topic Ideas")
async def api_get_topic_ideas(request: NicheRequest):
    """Takes a user-defined niche and returns a list of 6 potential viral topic ideas."""
    set_user_niche(request.niche)
    topic = await get_topic_ideas(request.niche)
    return {"content": topic}

@app.post("/research/topic", response_model=TextResponse, summary="Research a Specific Topic")
async def api_research_topic(request: TopicRequest, topic_selected : int =0 ):
    """Takes a single topic and performs in-depth research, returning a detailed report."""
    report = await research_topic(request.topic, topic_selected)
    return {"content":report}

@app.post("/generate/hook", response_model=TextResponse, summary="Generate a Hook")
async def api_generate_hook(request: HookRequest):
    """Takes a research report and generates a catchy hook for a video script."""
    hook = await generate_hook(request.research_report)
    return {"content": hook}

@app.post("/generate/script", response_model=TextResponse, summary="Generate a Script")
async def api_generate_script(request: ScriptRequest):
    """Takes a hook and a research report to generate a complete video script."""
    script = await generate_script(request.hook, request.research_report)
    return {"content": script}
