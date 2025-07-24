from agents.extensions.models.litellm_model import LitellmModel
from openai import AsyncOpenAI
import os



gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
    
    #gemini_model = OpenAIChatCompletionsModel(model = "gemini-2.0-flash", openai_client=gemini_client)
gemini_model = LitellmModel(model="gemini/gemini-2.5-flash")