from app.extensions import mongo

def create_user(username, number):
    # Check if user with this number already exists
    existing_number = mongo.db.users.find_one({"number": number})
    if existing_number:
        return "number"
    # Check if user with this username already exists
    existing_username = mongo.db.users.find_one({"username": username})
    if existing_username:
        return "username"
    from datetime import datetime, timezone
    user = {"username": username, "number": number, "created_on": datetime.now(timezone.utc)}
    result = mongo.db.users.insert_one(user)
    return str(result.inserted_id) 