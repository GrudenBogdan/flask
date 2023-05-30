from flask import Flask, request, render_template, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  #Secret key pentru Flash(Altfel nu primim message)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Flask/users_register.db'  # Cream SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True #Activeaza urmarirea modificarilor prin SQLLite database.
db = SQLAlchemy(app) #Leaga data de baze cu aplicatia.

# Cream modelul datei de baze (id = int(track numarul de utilizatori, name = username countului, password = parola, email = email.))
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))

# Cand deschidem site-ul ne arata direct login page-ul.
@app.route('/')
def home():
    return render_template('login.html')

# Apasand register end-point-ul este registerhtml.
@app.route('/register')
def new_account():
    return render_template('registerform.html')

# Primeste un username si o parola ca params si verifica daca exista deja in db.
def credentiale(username, password):
    user = User.query.filter_by(name=username).first()
    return user is not None

# Aici avem codul de login, daca username, password exista in database le luam cu request.form.get si ne da redirect catre dashboard, daca nu 
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # Daca credentialele se gasesc in db, ne redirecioaneaza catre dashnboard.html
    if credentiale(username, password):
        session['user'] = username # Va crea o sesiunea pentru user.
        return redirect('/dashboard')
    else: #Daca nu, primim eroare de mai jos, care a fost implementanta in html.
        return render_template('login.html', error='Invalid username or password.')

# Codul pentru pagina de register.
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username') #Primim de la user, username, pass, email.
    password = request.form.get('password')
    email = request.form.get('email')
    if User.query.filter_by(name=username).first() is not None: #Daca user-ul exista in db afisam eroarea.
        return render_template('registerform.html', error='Username already exists.')
    
    # Daca nu, in database, folosind variabila new_user adaugam unul nou
    new_user = User(name=username, password=password, email=email)
    db.session.add(new_user) #Adaugam.
    db.session.commit() #Aplicam modificarile asupra bazei de date.
    flash('Account created, return to the LOG IN page') #Afisam acest mesaj, folosind flash pe care il importam din flask si la care ne terbuie un secret.key.
    return render_template('registerform.html') 

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        user = session['user'] # Salvam informatii despre user, in cazul nostru username-ul sa putem sa ii dam display in nav-bar.
        return render_template('dashboard.html', user=user)
    else:
        return redirect('/login')
    
# Rutele catre fiecare pagina, utlizand template-urile din html.
@app.route('/login')
def return_to_login():
    return render_template('login.html')

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

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
    return render_template('add_a_post.html')

app.route('/dashboard')
def dashboard_return():
    return render_template('dashboard.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
