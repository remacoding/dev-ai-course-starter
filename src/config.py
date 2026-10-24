import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

SYSTEM_MESSAGE = """You are a university support assistant used for teaching.
For questions asking for a SAMPLE-AI workshop or project deadline, use the
lookup_course tool before answering.
Use the returned record as the source of the deadline.
Do not invent a deadline when the tool returns no record.
"""


@dataclass
class Config:
    """Simple configuration object reading environment variables."""

    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model_name: str = os.getenv("MODEL_NAME", "llama3.2")
    ollama_timeout: float = float(os.getenv("OLLAMA_TIMEOUT", "600"))


# Instantiate global configuration object
config = Config()