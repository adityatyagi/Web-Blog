from flask import Flask, render_template, request, session, make_response

from src.models.post import Post
from src.models.user import User
from src.common.database import Database
from src.models.blog import Blog


app = Flask(__name__)
app.secret_key = "Aditya"


# creating the endpoint
'''
CAN BE USED TO MAKE HOMEPAGE
@app.route('/l')  # 127.0.0.1:4995/login
def home_template():
    return render_template('base.html')
'''


@app.route('/')  # 127.0.0.1:4995/login
def login_template():
    return render_template('login.html')


@app.route('/register')   # 127.0.0.1:4995/register
def register_template():
    return render_template('register.html')


@app.before_first_request
def initialise_database():
    Database.initalise()


@app.route('/auth/login', methods=['POST'])  # the methods this endpoint is expecting
def login_user():
    #jsonObj = request.get_json()
    #print(jsonObj)
    #email = jsonObj['email']
    #print(email)
    #password = jsonObj['password']
    #print(password)

    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        #print('It is valid!')
        User.login(email)

    else:
        #print('It is not valid')
        session['email'] = None

    return render_template("profile.html", email=session['email'], password=password)
    # return jsonify(
    #     email=session['email'],
    #     password=password
    # )


@app.route('/auth/register', methods=["POST"])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)
    # session['email'] = email      -> as we have this thing set in the User.register()

    return render_template("profile.html", email=session['email'], password=password)


@app.route('/blogs/<string:user_id>')  # to access a particular user's blog
@app.route('/blogs')  # to access our own blog
def user_blogs(user_id=None):
    """ Get the blog of a particular user """
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])
    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email=user.email)


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template('posts.html', posts=posts, blog_title=blog.title, blog_id=blog._id)


@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        new_blog = Blog(user.email, title, description, user._id)
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))


@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):  # blog_id coming from the URL
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))

if __name__ == '__main__':
    app.run(port=4995)