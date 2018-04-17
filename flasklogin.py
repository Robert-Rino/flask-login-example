from flask import Flask, request, abort, redirect, Response, url_for, render_template, flash
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = u"please login first."
login_manager.init_app(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def to_json(self):
        result = {
            'username': self.username,
            'password': self.password,
        }
        return result

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def get_id(self):
        return self.username 

@app.route('/')
@app.route('/hello')
def index():
    return "<h2>Hello World</h2>"

@app.route('/home')
@login_required
def home():
    print current_user
    return render_template("home.html", current_user=current_user)

@app.route('/login' , methods=['GET' , 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            registeredUser = User.query.filter_by(username=username).first()
        except:
            print 'User {} not found !'.format(username)
            error = 'Invalid credentials'
            flash(error, 'errors')
            return render_template("login.html")
        if registeredUser and registeredUser.password == password:
            login_user(registeredUser)
            flash('You were successfully logged in','messages')
            return redirect(url_for('home'))
        else:
            error = 'Usrername or Password incorrect'
            flash(error, 'errors')
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        new_user.save_user()
        return render_template("login.html")
    else:
        return Response('''
            <h2>Register From</h2>
            <form action="" method="post">
            <p><input type=text name=username placeholder="Enter username">
            <p><input type=password name=password placeholder="Enter password">
            <p><input type=submit value=Login>
            </form>
        ''')

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

# callback to reload the user object
@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).first()

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
