from app.extensions import mongo

def create_user(username, number):
    user = {"username": username, "number": number}
    result = mongo.db.users.insert_one(user)
    return str(result.inserted_id) 