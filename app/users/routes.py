from flask import Blueprint, request, jsonify
from .schemas import UserSchema
from .services import create_user

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    errors = UserSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    user_id = create_user(data['username'], data['number'])
    return jsonify({"message": "User created", "user_id": user_id}), 201 