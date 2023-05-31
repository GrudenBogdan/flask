from flask import Flask, request, render_template, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

# Inițializarea aplicației Flask și configurarea bazei de date
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/PixelQA/PycharmProjects/LoginTemplate/flask/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WHOOSH_BASE'] = 'whoosh'
app.config['SQLALCHEMY_BINDS'] = {'two': 'sqlite:///C:/Users/PixelQA/PycharmProjects/LoginTemplate/flask/post_register.db'}
db = SQLAlchemy(app)

# Definirea claselor de model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))

class Two(db.Model):
    __bind_key__ = 'two'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(100))
    content = db.Column(db.String(2000))

# Definirea funcțiilor ajutătoare
def post_exists(title):
    post = Two.query.filter_by(title=title).first()
    return post is not None

def credentiale(username, password):
    user = User.query.filter_by(name=username).first()
    if user and check_password_hash(user.password, password):
        return True
    return False

# Definirea rutelor și funcțiilor asociate
@app.route('/')
def home():
    return render_template('auth/login.html')

@app.route('/register')
def new_account():
    return render_template('auth/registerform.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(name=username).first()
    if user and check_password_hash(user.password, password):
        session['user'] = username
        return redirect('/dashboard')
    else:
        return render_template('auth/login.html', error='Invalid username or password.')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    if User.query.filter_by(name=username).first() is not None:
        return render_template('auth/registerform.html', error='Username already exists.')
    password_hash = generate_password_hash(password)
    new_user = User(name=username, password=password_hash, email=email)
    db.session.add(new_user)
    db.session.commit()
    flash('Account created, return to the LOG IN page')
    return render_template('auth/registerform.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        user = session['user']
        return render_template('base.html', user=user)
    else:
        return redirect('/login')

@app.route('/viewposts')
def viewposts():
    allPosts = Two.query.all()
    return render_template('blog/allposts.html', allPosts=allPosts)

@app.route('/addapost', methods=['POST'])
def register_post():
    title = request.form.get('title')
    author = request.form.get('author')
    content = request.form.get('content')
    if post_exists(title):
        flash('Post with the same title already exists.', 'error')
        return redirect('/addapost')
    new_post = Two(title=title, author=author, content=content)
    db.session.add(new_post)
    db.session.commit()
    flash('Post added successfully.')
    return redirect('/addapost')

@app.route('/login')
def return_to_login():
    return render_template('auth/login.html')

@app.route('/forgot-password')
def forgot_password():
    return render_template('auth/forgot_password.html')

@app.route('/forgot-password', methods=['POST'])
def reset_password():
    return redirect('/login')

@app.route('/back-to-login')
def back_to_login():
    return redirect('/login')

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route("/addapost")
def addapost():
    return render_template('blog/add_a_post.html')

# Blocul if __name__ == '__main__':
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
