from pymongo.errors import ServerSelectionTimeoutError
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


MONGO_URL=os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv(
    "MONGODB_DATABASE",
    "customer_support",
)

if not  MONGO_URL:
    raise ValueError("MONGO_URL is missing from .env")

client=MongoClient(
    MONGO_URL,
    ServerSelectionTimeoutMS=5000,
)


db=client[DATABASE_NAME]

orders_collection = db["orders"]
refunds_collection = db["refunds"]
escalations_collection=db["escalations_collection"]


def check_connection() -> bool:
    """Check whether MongoDB is reachable."""
    client.admin.command("ping")
    return True