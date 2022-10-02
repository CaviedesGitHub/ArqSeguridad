from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse

from ..forms import SignupForm, LoginForm
from ..modelos import db, User, UsuarioSchema
from auth_ms import app

from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token


usuario_schema = UsuarioSchema()

class VistaLogIn(Resource):
    def post(self):
        u_email = request.json["email"]
        u_password = request.json["password"]
        print(request.json["email"])
        print(request.json["password"])
        usuario = User.query.filter_by(email=u_email, password = u_password).first()
        print(usuario_schema.dumps(usuario))
        if usuario:
            login_user(usuario, remember=True)
            token_de_acceso=create_access_token(identity=usuario.id)
            return {"mensaje":'Inicio de sesión exitoso', "token_de_acceso":token_de_acceso}
        else:
            return {'mensaje':'Nombre de usuario o contraseña incorrectos'}, 401


class VistaSignIn(Resource):
    
    def post(self):
        nuevo_usuario = User(name=request.json["name"], password=request.json["password"], email=request.json["email"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso=create_access_token(identity=nuevo_usuario.id)
        return {"mensaje":'Usuario creado exitosamente', "token_de_acceso":token_de_acceso}
        #return 'Usuario creado exitosamente', 201

    def put(self, id_usuario):
        usuario = User.query.get_or_404(id_usuario)
        usuario.name = request.json.get("name",usuario.name)
        usuario.contrasena = request.json.get("contrasena",usuario.contrasena)
        usuario.email = request.json.get("email",usuario.email)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = User.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '',204


