__author__ = 'laurenbanawa'

import uuid
import datetime

from flask import session
from src.common.database import Database
from src.models.blog import Blog


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    # Use a class method instead of self because we won't yet have the User object when searching by email
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

    # Check whether a user's email matches the password they sent us
    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None: # aka the user was found
            # check the password
            return user.password == password
        return False

    # create a user if one does not already exist
    @classmethod
    def register(cls, email, password):
        user = User.get_by_email(email)
        if user is None:
            # User doesn't exist, so we can create it
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # User exists :(
            return False

    @staticmethod
    def login(user_email):
        # login_valid has already been called, so we know user has valid email and password
        # store the email in the session -- if the session does not have an email, the user has not logged in
        # to prevent other users from changing emails and passwords that aren't theirs
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    # find all blogs by a specific author
    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    # create a new blog
    def new_blog(self, title, description):
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)
        blog.save_to_mongo()

    # create a new post
    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)

    def json(self):
        return {
            "email": self.email,
            "_id": self._id,
            "password": self.password
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())