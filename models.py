from datetime import datetime

from app import db
from hashutils import make_pw_hash


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
    user_name = db.Column(db.String(50))
    email_address = db.Column(db.String(128), unique=True)
    pw_hash = db.Column(db.String(120))
    blog_posts = db.relationship(BlogPost, backref='owner')

    def __init__(self, user, email, password):
        self.user_name = user
        self.email_address = email
        self.pw_hash = make_pw_hash(password)
