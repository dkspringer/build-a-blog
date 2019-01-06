import hashlib
import json
import random
import string
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

with open('params.json') as file:
    params = json.load(file)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    params.get('user'),
    params.get('password'),
    params.get('ip'),
    params.get('port'),
    params.get('db_name')
)
db = SQLAlchemy(app)


################################################################################
# Functions for creating and verifying password hash
################################################################################

def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])


def make_pw_hash(password, salt=None):
    if not salt:
        salt = make_salt()
    hash = hashlib.sha256(str.encode(password + salt)).hexdigest()
    return '{},{}'.format(hash, salt)


def check_pw_hash(password, hash):
    salt = hash.split(',')[1]
    if make_pw_hash(password, salt) == hash:
        return True
    return False


################################################################################
# Database models
################################################################################

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    date = db.Column(db.DateTime)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.date = datetime.now()


# TODO: finish linking to BlogPost; drop existing tables and create new ones
"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    email_address = db.Column(db.String(128), unique=True)
    pw_hash = db.Column(db.String(120))
    blog_posts = db.relationship(BlogPost, backref='owner')

    def __init__(self, user, email, password):
        self.user_name = user
        self.email_address = email
        self.pw_hash = make_pw_hash(password)
"""


################################################################################
# Routing functions
################################################################################

@app.route('/create-new-entry')
def create_post():
    return render_template('new-post.html', title='Create New Post')


@app.route('/submit-post', methods=['POST'])
def add_post():
    post_title = request.form.get('post-title')
    post_body = request.form.get('post-body')

    # Check if content has been provided for both title and body of post
    error = ''
    if not post_title:
        error += 'You must provide a title for your post.  '
    if not post_body:
        error += 'You must provide some text for your post.  '

    if error:
        return render_template('new-post.html', title='Create New Post',
                               post_title=post_title, post_body=post_body,
                               error=error)

    # Add blog post to the database
    new_post = BlogPost(post_title, post_body)
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('view_post', post_id=new_post.id))


@app.route('/view-post', methods=['GET'])
def view_post():

    id = request.args.get('post_id')
    blog_post = BlogPost.query.get(id)

    return render_template('view-post.html', blog_post=blog_post)

@app.route('/users', methods=['GET'])
def users():
    return render_template('users.html')

@app.route('/showRegister', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


# TODO: Add code to add new user

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        post_title = request.form.get('post-title')
        post_body = request.form.get('post-body')

        new_post = BlogPost(post_title, post_body)
        db.session.add(new_post)
        db.session.commit()

    posts = BlogPost.query.all()
    return render_template('main.html', title='home', blog_posts=posts)


if __name__ == '__main__':
    app.run()