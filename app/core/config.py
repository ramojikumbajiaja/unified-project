from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
REFRESH_SECRET = os.getenv("REFRESH_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_EXPIRE_SECONDS = int(os.getenv("ACCESS_EXPIRE_SECONDS", 1800))
REFRESH_EXPIRE_SECONDS = int(os.getenv("REFRESH_EXPIRE_SECONDS", 1209600))
