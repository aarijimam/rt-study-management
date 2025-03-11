import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/study_db")

config = Config()