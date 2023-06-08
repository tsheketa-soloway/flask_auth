from app import db
from models import User
from schemas import UserSchema

def create_user(data):
    new_user = UserSchema().load(data)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_all_users():
    all_users = User.query.all()
    return all_users

def get_user(id):
    user = User.query.get(id)
    return user

def update_user(id, data):
    user = User.query.get(id)
    update_data = UserSchema().load(data, instance=user, partial=True)
    db.session.commit()
    return update_data

def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user
