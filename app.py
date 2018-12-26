from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:yHXfmphcFDE7GpUc@localhost:8889/build-a-blog'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/create-new-entry')
def add_blog_entry():
    return render_template('new-post.html', title='Create New Post')

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        post_title = request.form.get('post-title')
        post_body = request.form.get('post-body')

        new_post = BlogPost(post_title, post_body)
        db.session.add(new_post)
        db.session.commit()

    blog_posts = BlogPost.query.all()
    return render_template('main.html', title='Build A Blog', blog_posts=blog_posts)


if __name__ == '__main__':
    app.run()
