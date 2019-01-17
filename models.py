from datetime import datetime

from app import db
from hashutil import make_hash_with_salt


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    date = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.date = datetime.now()
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    email_address = db.Column(db.String(128), unique=True)
    pw_hash = db.Column(db.String(120))
    blog_posts = db.relationship(BlogPost, backref='owner')
    img_file = db.Column(db.String(100), default='default.jpg')

    def __init__(self, user, email, password, img_file):
        self.user_name = user
        self.email_address = email
        self.pw_hash = make_hash_with_salt(password)
        self.img_file = img_file
