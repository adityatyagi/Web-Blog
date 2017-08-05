from src.common.database import Database
from src.models.blog import Blog
import datetime
import uuid
from flask import session


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        """ to get the users from the database by filtering by the email """
        data = Database.find_one(collection="users", query={"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, id):
        """  to get the users from the database by filtering by the id """
        data = Database.find_one(collection="users", query={"_id": id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        """
        Validation of the login credentials
        Check whether the users email matches the password they sent us
        """
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password  # Check the password
        else:
            return False

    @classmethod
    def register(cls, email, password):
        """ Registering/SignUp new user """
        user = cls.get_by_email(email)  # checking if the user's email-id already exists
        if user is None:
            # User doesn't exist, so we can create it
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            # User already exists by this email-id
            return False

    @staticmethod
    def login(user_email):
        """ Login with your username and password"""
        session['email'] = user_email

    @staticmethod
    def logout():
        """ Logout of the app """
        session['email'] = None

    def get_blogs(self):
        """ Get the blogs """
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        """
        The data will come from the website
        the user has to enter the title, description from a form
        the author_id and author will come from there sessions
        """
        blog = Blog(author=self.email, title=title, description=description, author_id=self._id)
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title, content=content, date=date)


    def json(self):
        return {
            "email": self.email,
            "_id": self._id,
            "password": self.password  # TODO: this is not safe
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())

'''
Cookie: A way to store information on the web browser

Session: The login() will be called after the login_valid() is called.
This tells that the user credentials matches and he must be logged in now.
Once this is done, we store their email in the session.

WHAT'S HAPPENING?
The next time the user requests, they will send us a UNIQUE IDENTIFIER in their cookie.
This cookie will be able to identify this session and this session will then store the email.
Because in step 1 we stored the email in the session, the server will be able to identify this
particular requests.

If the session does not have email therefore, the user is not logged in.


REGISTER

After the user has registered successfully, we store the email in the session.
Because after the registration is completed, always the login page comes in

Flask does the cookies for us
Whenever the user access our application, flask sends them a cookie which is secure and which
uniquely identifies the session

We should not exchange the password information over the network but internally we can do
'''

