from auth_ms import create_app
from flask_login import login_manager

from flask import render_template, request, redirect, url_for, abort
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse

from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .forms import LoginForm, SignupForm
from .modelos import db, User
from .vistas import VistaLogIn, VistaSignIn

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

login_manager = LoginManager(app)

cors=CORS(app)

api = Api(app)
api.add_resource(VistaSignIn, '/apisignin')
api.add_resource(VistaLogIn, '/apilogin')

jwt=JWTManager(app)

@app.route("/")
def hola_mundo():
    return "Hola, Mundo!!. v2"

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route("/index")
def index():
    return render_template("index.html")    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template("signup_form.html", form=form, error=error)

