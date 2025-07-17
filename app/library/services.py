from app.extensions import mongo
from datetime import datetime, timezone

LIBRARY_COLLECTION = "library"

def add_library_item(url, user_id, file_type, category):
    item = {
        "url": url,
        "user_id": user_id,
        "type": file_type,
        "category": category,
        "created_at": datetime.now(timezone.utc)
    }
    result = mongo.db[LIBRARY_COLLECTION].insert_one(item)
    return str(result.inserted_id)

def get_library_items(page=1, per_page=10):
    skip = (page - 1) * per_page
    cursor = mongo.db[LIBRARY_COLLECTION].find().sort("created_at", -1).skip(skip).limit(per_page)
    items = list(cursor)
    for item in items:
        item["_id"] = str(item["_id"])
    total = mongo.db[LIBRARY_COLLECTION].count_documents({})
    total_pages = (total + per_page - 1) // per_page
    return items, total, total_pages 