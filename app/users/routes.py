from flask import Blueprint, request, jsonify
from .schemas import UserSchema
from .services import create_user
from app.extensions import mongo
from bson import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from bson.objectid import ObjectId, InvalidId

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
@jwt_required()
def add_user():
    """
    Create a new user
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - number
          properties:
            username:
              type: string
            number:
              type: string
    responses:
      201:
        description: User created
      409:
        description: Username or phone number already in use
      400:
        description: Validation error
    """
    data = request.get_json()
    errors = UserSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    user_id = create_user(data['username'], data['number'])
    if user_id == "number":
        return jsonify({"error": "Phone number already in use"}), 409
    if user_id == "username":
        return jsonify({"error": "Username already in use"}), 409
    if user_id is None:
        return jsonify({"error": "User creation failed"}), 500
    return jsonify({"message": "User created", "user_id": user_id}), 201

@users_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        obj_id = ObjectId(user_id)
    except (InvalidId, TypeError):
        return jsonify({'error': 'Invalid user id'}), 400
    user = mongo.db.users.find_one({"_id": obj_id})
    if not user:
        return jsonify({"error": "User not found"}), 404
    user["_id"] = str(user["_id"])
    return jsonify(user), 200

@users_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    identity = get_jwt_identity()  # This will be the phone number if that's what you used
    user = mongo.db.users.find_one({"number": identity})
    if not user:
        return jsonify({"error": "User not found"}), 404
    user["_id"] = str(user["_id"])
    return jsonify(user), 200 