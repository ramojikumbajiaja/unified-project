from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./unified.db")
ACCESS_SECRET = os.getenv("ACCESS_SECRET", "change_me")
REFRESH_SECRET = os.getenv("REFRESH_SECRET", "change_me_refresh")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_EXPIRE_SECONDS = int(os.getenv("ACCESS_EXPIRE_SECONDS", 1800))
REFRESH_EXPIRE_SECONDS = int(os.getenv("REFRESH_EXPIRE_SECONDS", 1209600))
