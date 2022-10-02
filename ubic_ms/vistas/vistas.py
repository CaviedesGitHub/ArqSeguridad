from flask import Flask, jsonify, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false, true
from werkzeug.urls import url_parse

from ..modelos import db, Ubicacion, UbicacionSchema
from auth_ms import app

from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError
from functools import wraps
from jwt import InvalidSignatureError

from celery import Celery
from datetime import datetime

celery_app=Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task(name='registrar_log')
def registrar_log(*args):
    pass


ubicacion_schema = UbicacionSchema()

class VistaUbicaciones(Resource):
    @jwt_required()
    def get(self):
        return [ubicacion_schema.dump(ubic) for ubic in Ubicacion.query.all()]

    def post(self, id_usuario):
        nueva_ubic = Ubicacion(direccion=request.json["direccion"], zona=request.json["zona"], 
                               id_usuario=id_usuario)
        db.session.add(nueva_ubic)
        db.session.commit()
        return ubicacion_schema.dump(nueva_ubic)

class VistaUbicacion(Resource):
    def get(self, id_ubic):
        ubicacion = Ubicacion.query.get_or_404(id_ubic)
        db.session.commit()
        return ubicacion_schema.dump(ubicacion)
    
    def put(self, id_ubic):
        ubicacion = Ubicacion.query.get_or_404(id_ubic)
        ubicacion.name = request.json.get("direccion", ubicacion.direccion)
        ubicacion.zona = request.json.get("zona", ubicacion.zona)
        ubicacion.id_usuario = request.json.get("id_usuario", ubicacion.id_usuario)
        db.session.commit()
        return ubicacion_schema.dump(ubicacion)

    def delete(self, id_ubic):
        ubicacion = Ubicacion.query.get_or_404(id_ubic)
        db.session.delete(ubicacion)
        db.session.commit()
        return '',204

def authorization_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()          
                user_url=request.path[-1:]
                user_jwt=str(int(get_jwt_identity()))
                if user_jwt==user_url:
                    argsX=(get_jwt_identity(), datetime.utcnow(), 1)
                    registrar_log.apply_async(args=argsX, queue='logs')
                    return fn(*args, **kwargs)
                else:
                    args=(get_jwt_identity(), datetime.utcnow(), 5)
                    registrar_log.apply_async(args=args, queue='logs')
                    return "Ataque Detectado"
                #claims = get_jwt()
                #if claims["is_administrator"]:
                #    return fn(*args, **kwargs)
                #else:
                #    return "Admins only!"
            except InvalidSignatureError:
                args=('Invalido', datetime.utcnow(), 2)
                registrar_log.apply_async(args=args, queue='logs')
                return "Signature verification failed"
            except NoAuthorizationError:
                args=('Inexistente', datetime.utcnow(), 3)
                registrar_log.apply_async(args=args, queue='logs')
                return "Missing JWT"
            except Exception as inst:
                print(type(inst))    # the exception instance
                print(inst.args)     # arguments stored in .args
                print(inst)
                args=('Invalido', datetime.utcnow(), 4)
                registrar_log.apply_async(args=args, queue='logs')
                return "Usuario Desautorizado"

        return decorator

    return wrapper

class VistaUbicacionesUsuario(Resource):
    @authorization_required()
    def get(self, id_usuario):
        return [ubicacion_schema.dump(ubic) for ubic in Ubicacion.query.filter_by(id_usuario=id_usuario)]

    #@claims_verification_loader()
    #@jwt.claims_verification_loader()
    def verifica_claims():
        return true




