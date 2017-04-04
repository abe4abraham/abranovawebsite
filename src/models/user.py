import uuid
from flask import session
from src.common.database import Database

__author__ = 'Abraham'


class User(object):
    def __init__(self, name, email, _id=None):
        self.name = name
        self.email = email
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)


    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(name, email):
        user = User.get_by_email(email)
        if user is not None:
            return user.name == name
        return False

    @classmethod
    def register(cls, email, name):
        user = cls.get_by_email(email)

        if user is None:
            new_user = cls(email, name)
            new_user.save_to_mongo()
            session['email'] = email
            return True

        else:

            return False

    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def json(self):
        return{
            "email": self.email,
            "_id": self._id,
            "name": self.name
            }

    def save_to_mongo(self):
        Database.insert("users", self.json())