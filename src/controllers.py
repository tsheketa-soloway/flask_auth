from flask import request, jsonify
from app import app, auth
from models import User
from schemas import UserSchema
from services import *
from werkzeug.security import check_password_hash

@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not check_password_hash(user.password_hash, password):
            return False
    return True

@app.route("/api/users", methods=["POST"])
def add_user():
    try:
        new_user = create_user(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    return UserSchema().jsonify(new_user), 201

@app.route("/api/users", methods=["GET"])
@auth.login_required
def get_users():
    all_users = get_all_users()
    result = UserSchema.dump(all_users)
    return jsonify(result)

@app.route("/api/users/<id>", methods=["GET"])
@auth.login_required
def user_detail(id):
    user = get_user(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return UserSchema().jsonify(user)

@app.route("/api/users/<id>", methods=["PUT"])
@auth.login_required
def user_update(id):
    user = get_user(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    try:
        update_data = update_user(id, request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    return UserSchema().jsonify(update_data)

@app.route("/api/users/<id>", methods=["DELETE"])
@auth.login_required
def user_delete(id):
    user = get_user(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    delete_user(id)
    return jsonify({"message": "User deleted successfully"})

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})
