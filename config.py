"""
config.py - Central Configuration
Loads environment variables and provides settings for the entire application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =============================================================================
# API KEYS
# =============================================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# Set for LangChain
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

# =============================================================================
# TELEGRAM SETTINGS
# =============================================================================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
os.environ["TELEGRAM_BOT_TOKEN"] = TELEGRAM_BOT_TOKEN


# =============================================================================
# SERVER SETTINGS
# =============================================================================

PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "https://polite-areas-tickle.loca.lt")

# =============================================================================
# MODEL SETTINGS
# =============================================================================

# Default LLM model to use
DEFAULT_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
DEFAULT_TEMPERATURE = 0

# =============================================================================
# VALIDATION
# =============================================================================

def validate_config():
    """Check that required configuration is present."""
    missing = []
    if not GROQ_API_KEY or GROQ_API_KEY == "":
        missing.append("GROQ_API_KEY")
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "":
        missing.append("TELEGRAM_BOT_TOKEN")
    
    if missing:
        print(f"⚠️  Warning: Missing environment variables: {', '.join(missing)}")
        print("   Please set them in your .env file.")
        return False
    return True
