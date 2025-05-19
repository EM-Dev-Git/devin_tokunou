import os
import logging
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

env_path = os.path.join(BASE_DIR, 'env', '.env')
load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "sk-dummy-api-key-for-development-purposes-only")

CORS_ALLOW_ORIGINS = os.environ.get("CORS_ALLOW_ORIGINS", "*").split(",")
CORS_ALLOW_CREDENTIALS = os.environ.get("CORS_ALLOW_CREDENTIALS", "True").lower() == "true"
CORS_ALLOW_METHODS = os.environ.get("CORS_ALLOW_METHODS", "*").split(",")
CORS_ALLOW_HEADERS = os.environ.get("CORS_ALLOW_HEADERS", "*").split(",")

SERVER_HOST = os.environ.get("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.environ.get("SERVER_PORT", "8000"))
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
