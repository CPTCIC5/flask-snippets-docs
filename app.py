from flask import Flask,render_template,flash,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)


class User(db.Model):
    username = db.Column(db.String(50),unique=True)

"""
@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name,content=['time','joee','bill'])
"""


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        image = request.files['image']
        return flash('Req Sent!')
    return render_template('login.html')



@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


@app.route('/user/<string:username>')
def profile(username):
    return f'{username}\'s profile'


if __name__ == "__main__":
    app.run(debug=False)