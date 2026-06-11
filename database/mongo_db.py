#unstructured data for chat history and analytics,tool ouputs and agent traces
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os
import certifi

load_dotenv()

client = None
db = None
chat_collection = None
analytics_collection = None

def init_db():
    global client,db,chat_collection, analytics_collection
    # Connect to MongoDB
    client = MongoClient(
                os.getenv("MONGO_URI"),
                serverSelectionTimeoutMS=10000,
    )
     # Create database
    db = client["travel_bot"]

    # Create collections
    chat_collection = db["chat_history"]
    analytics_collection = db["analytics"]

# Save analytics data
def save_analytics(query, category="general", destination="unknown"):

    data = {
        "query": query,
        "category": category,
        "destination": destination,
        "timestamp": datetime.now()
    }
    analytics_collection.insert_one(data)

def save_message(session_id, role, message):
    try:
        chat_collection.insert_one({
            "session_id": session_id,
            "role": role,
            "message": message,
            "timestamp": datetime.now()
         })
    except Exception as e:
       print("MongoDB save_message error:", e)

def load_chat_history(session_id):
    return list(chat_collection.find({"session_id": session_id}))

def clear_history(session_id):
    chat_collection.delete_many({"session_id": session_id})