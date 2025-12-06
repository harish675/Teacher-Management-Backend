import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB Configuration
mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
db_name = os.getenv("DB_NAME", "kevin_assignment_db")

# Server Configuration
port = int(os.getenv("PORT", "8000"))
api_prefix = os.getenv("API_PREFIX", "/rent-easy/api")

# Environment
environment = os.getenv("ENVIRONMENT", "development")