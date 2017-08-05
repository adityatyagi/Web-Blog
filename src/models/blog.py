import uuid
import datetime
from src.models.post import Post
from src.common.database import Database


class Blog(object):
    """ Using the _id, we overwrite the default id given to data by the mongodb"""
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.author_id = author_id
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        """ Ask the user to enter the details of the new posts
         Will Handle the POST request coming from the browser """
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)
        post.save_to_mongo()

    def get_posts(self):
        """ Get all the posts for a particular blog, identified by its blog_id """
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        """ Save the blog to the database """
        Database.insert(collection='blogs', data=self.json())

    def json(self):
        """ JSON representation of the data"""
        return {
            'author': self.author,
            'author_id': self.author_id,
            'title': self.title,
            'description': self.description,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, id):
        """ Get the blog data, it returns a object of type blog """
        blog_data = Database.find_one(collection='blogs', query={'_id': id})  # this will return the author, title, description, id and cls=current class
        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        """ This will return a list of Blog() objects """
        blogs = Database.find(collection="blogs", query={'author_id': author_id})
        return [cls(**blog) for blog in blogs]  #TODO UNDERSTAND THIS


        #return cls(author=blog_data['author'],
        #           title=blog_data['title'],
        #           description=blog_data['description'],
        #           id=blog_data['_id'])


    '''
    @staticmethod
    def get_from_mongo():
        """ Get the  Blog Data """
        blog_data =  Database.find_one(collection='blogs', query={'id': id})
        return blog_data


    With the static method, we would be able to return only the blog data fields, we wont be able
    to access the post fields. Therefore, we generalise it and use the @classmethod, wherein we 
    return OBJECT of type Blog(), instead of just the data

    '''

