from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

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


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    date = db.Column(db.DateTime)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.date = datetime.now()


@app.route('/create-new-entry')
def create_post():
    return render_template('new-post.html', title='Create New Post')


@app.route('/submit-post', methods=['POST'])
def add_post():
    post_title = request.form.get('post-title')
    post_body = request.form.get('post-body')

    # Check if content has been provided for both title and body of post
    title_error = ''
    body_error = ''
    if not post_title:
        title_error = 'You must provide a title for your post'
    if not post_body:
        body_error = 'You must provide some text for your post'

    if title_error or body_error:
        return render_template('new-post.html', title='Create New Post',
                               post_title=post_title, post_body=post_body,
                               title_error=title_error, body_error=body_error)

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