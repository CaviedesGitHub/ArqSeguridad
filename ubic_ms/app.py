from sqlalchemy import false
from ubic_ms import create_app
from flask_login import login_manager

from flask import render_template, request, redirect, url_for, abort
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse

from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .modelos import db, Ubicacion
from .vistas import VistaUbicacion, VistaUbicaciones, VistaUbicacionesUsuario

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

#login_manager = LoginManager(app)

cors=CORS(app)

jwt=JWTManager(app)

api = Api(app)
api.add_resource(VistaUbicacion, '/ubicacion/<int:id_ubic>')
api.add_resource(VistaUbicaciones, '/ubicaciones')
api.add_resource(VistaUbicacionesUsuario, '/ubicacionesusuario/<int:id_usuario>')

#@jwt.token_verification_loader()   
def verifica_claims(jwt_payload: dict):
    print("Verifica Claims")
    return false


