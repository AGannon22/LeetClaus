import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(
    host=os.getenv("MONGO_HOST", "localhost"),
    port=int(os.getenv("MONGO_PORT", "27017")),
    username=os.getenv("MONGO_USER", "root"),
    password=os.getenv("MONGO_PASSWORD", "rootpassword"),
)

auth_db = client[os.getenv("AUTH_DB_NAME", "leetclause_auth")]  # logins
data_db = client[os.getenv("DATA_DB_NAME", "leetclause_data")]  # everything else
