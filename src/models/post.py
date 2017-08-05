import datetime
import uuid

from src.common.database import Database


class Post(object):

    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), _id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert('posts', self.json())

    def json(self):
        return {
            '_id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }

    @classmethod
    def from_mongo(cls, ind: object) -> object:
        """ Returning an object of type Post() """
        post_data = Database.find_one(collection='posts', query={'_id': ind})
        return cls(**post_data)
        # for each of the element in post data, get the name of every element in post_data from DB
        # and say that object's element is equal to that


        #return cls(blog_id=post_data['blog_id'],
        #           title=post_data['title'],
        #           content=post_data['content'],
        #           author=post_data['author'],
        #           created_date=post_data['created_date'],
        #           _id=post_data['_id'])



    @staticmethod
    def from_blog(ind):
        return [post for post in Database.find(collection='posts', query={'blog_id': ind})]

