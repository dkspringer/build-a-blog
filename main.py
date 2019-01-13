from flask import render_template, request, redirect, url_for, session

from app import app, db
from hashutils import check_pw_hash
from models import User, BlogPost


@app.route('/create-new-entry')
def create_post():
    return render_template('new-post.html', title='Create New Post')


@app.route('/submit-post', methods=['POST'])
def add_post():
    post_title = request.form.get('post-title')
    post_body = request.form.get('post-body')
    owner = User.query.filter_by(email_address=session['email']).first()

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
    new_post = BlogPost(post_title, post_body, owner)
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
    return render_template('users.html', users=User.query.all())


@app.route('/user/<email>')
def user_posts(email):
    owner = User.query.filter_by(email_address=email).first()
    posts = BlogPost.query.filter_by(owner=owner).all()

    username = User.query.filter_by(email_address=email).first().user_name
    return render_template('user-posts.html', user=username, blog_posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        user = request.form.get('user')
        email = request.form.get('email')
        password = request.form.get('password')
        verify = request.form.get('verify')

        # TODO: validate registration input

        # TODO: add user
        new_user = User(user, email, password)
        db.session.add(new_user)
        db.session.commit()
        session['email'] = email
        return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        email = request.form.get('email')
        pw = request.form.get('password')

        user = User.query.filter_by(email_address=email).first()
        if user and check_pw_hash(pw, user.pw_hash):
            session['email'] = email
            return redirect('/')
        return '<h1>NO MATCH...</h1>'

    return render_template('login.html')

    # TODO: If email and password match: start session for user
    # TODO: redirect to previous page


@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')


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


@app.context_processor
def inject_session():
    return dict(session=session)


@app.context_processor
def inject_user():
    return dict(User=User)


@app.context_processor
def inject_posts():
    return dict(BlogPost=BlogPost)


if __name__ == '__main__':
    app.run(debug=True)
