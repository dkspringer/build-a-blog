from flask import render_template, request, redirect, url_for, session, flash

from app import app, db
from hashutil import verify_hash
from models import User, BlogPost
from validation import passwords_match, is_valid_username, is_valid_password, \
    is_valid_email, user_exists


@app.route('/create-new-entry')
def create_post():
    return render_template('new-post.html', title='Create New Post')


@app.route('/submit-post', methods=['POST'])
def add_post():
    post_title = request.form.get('post-title')
    post_body = request.form.get('post-body')
    owner = User.query.filter_by(user_name=session['user_name']).first()

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


@app.route('/user/<username>')
def user_posts(username):
    owner = User.query.filter_by(user_name=username).first()
    posts = BlogPost.query.filter_by(owner=owner).all()

    return render_template('user-posts.html', username=username,
                           blog_posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        user = request.form.get('user')
        email = request.form.get('email')
        password = request.form.get('password')
        verify = request.form.get('verify')

        # Check for errors in new user validation
        error = False
        if user_exists(user, email):
            flash('Username or email address is already in use')
            # Do not perform any further checks
            return render_template('register.html')
        if not is_valid_username(user):
            flash('Invalid user name: must be between 5 and 32 characters with '
                  'no spaces')
            error = True
        if not is_valid_email(email):
            flash('The email provided is not a valid email address')
            error = True
        if not passwords_match(password, verify):
            flash('Passwords do not match')
            error = True
        if not is_valid_password(password):
            flash('Invalid password: must be between 8 and 64 characters with '
                  'no spaces')
            error = True

        # If errors, redisplay registration pages, else create new user
        if error:
            return render_template('register.html')
        else:
            new_user = User(user, email, password)
            db.session.add(new_user)
            db.session.commit()
            session['user_name'] = user
            return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        username = request.form.get('username')
        pw = request.form.get('password')

        user = User.query.filter_by(user_name=username).first()
        if user and verify_hash(pw, user.pw_hash):
            session['user_name'] = username
            return redirect('/')
        else:
            flash('User does not exist or user name and password do not match')

    return render_template('login.html')


@app.route('/logout')
def logout():
    del session['user_name']
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


if __name__ == '__main__':
    app.run(debug=True)
