from app.extensions import mongo
from datetime import datetime, timezone

LIBRARY_COLLECTION = "library"

def add_library_item(url, user_id):
    item = {
        "url": url,
        "user_id": user_id,
        "created_at": datetime.now(timezone.utc)
    }
    result = mongo.db[LIBRARY_COLLECTION].insert_one(item)
    return str(result.inserted_id) 