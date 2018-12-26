from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:yHXfmphcFDE7GpUc@localhost:8889/build-a-blog'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

@app.route('/')
def hello_world():
    return render_template('main.html')


if __name__ == '__main__':
    app.run()
