import sqlite3
from db import db
# Python Model. class 'User' is an Helper class. The model is an internal representation of an entity


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)  # insert 1 object (self)
        db.session.commit()  # commit change


    @classmethod  # so replace class name User with cls
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()  # SELECT * FROM items WHERE username=username LIMIT 1


    @classmethod  # so replace class name User with cls
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

