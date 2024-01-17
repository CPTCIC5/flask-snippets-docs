from flask import Flask,render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy


app= Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db =SQLAlchemy(app)


class Posts(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),nullable=False)
    subtitle=db.Column(db.String(100),nullable=True)
    content=db.Column(db.String(250),nullable=False)
    slug=db.Column(db.String(25),nullable=False)

    def __repr__(self):
        return self.title


@app.route('/add-post',methods =['GET','POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        content = request.form['content']
        slug = request.form['slug']
        entry = Posts(title=title,subtitle=subtitle,content=content,slug=slug)
        db.session.add(entry)
        db.session.commit()
        return "xyz"
    return render_template('post.html')


@app.route('/post/<int:sno>')
def post(sno):
    queryset= Posts.query.filter_by(sno=sno).first()
    return render_template('particular_post.html',queryset=queryset)


@app.route('/all-posts')
def all_posts():
    all_sets= Posts.query.all()
    return render_template('post_read.html',all_sets=all_sets)


@app.route('/edit/<int:sno>')
def edit(sno):
    query= Posts.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        sno.title = request.form.get('title',sno.title)
        sno.subtitle = request.form.get('subtitle',sno.subtitle)
        sno.content = request.form.get('content',sno.content)
        sno.slug = request.form.get('slug',sno.slug)
        db.session.add(query)
        db.session.commit()
        return "xyz"
    return "xyz"


@app.route('/delete/<int:sno>')
def delete_post(sno):
    x1=Posts.query.filter_by(sno=sno)
    if x1:
        x1.delete()
        db.session.commit()
        
        return "delete hogay"
    else:
        return "Doesnt exist"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login',methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password= request.form['password']
        return redirect(url_for("user",usr=user))
    return render_template('login.html')


@app.route("/<string:usr>")
def user(usr):
    return f"<h1> {usr} </h1>"


@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)