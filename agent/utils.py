import os
import pathlib
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

def get_key(name: str) -> str:
    """Grab an API key by name. Raises an error if it's missing. """
    value = os.getenv(name)
    if not value: 
        raise ValueError(f"Missing API key: + {name}. Check your .env file.")
    return value
    
