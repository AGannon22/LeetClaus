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

db = client[os.getenv("DB_NAME", "leetclause")]

auth = db["auth"]            # logins: username + password hash
user_data = db["user_data"]  # everything else about a user

# Mongo itself rejects a second account with the same username (safe to run every startup).
auth.create_index("username", unique=True)
user_data.create_index("username", unique=True)  # one progress document per user
