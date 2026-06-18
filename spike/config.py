import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# API Credentials
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Retrieval Hyperparameters & Constants
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 3
DATA_FOLDER = "docs"
