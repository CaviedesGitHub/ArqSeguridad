from base64 import b64encode
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, decode_token, get_jwt, get_jwt_header, get_unverified_jwt_headers
from flask_jwt_extended import JWTManager
from itsdangerous import base64_encode

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "frase-secreta"  # Change this!  frase-secreta secret-jwt
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
jwt = JWTManager(app)
api = Api(app)

class AuthResource(Resource):
    def get(self):
        access_token = create_access_token(identity="test")
        return jsonify(access_token=access_token)

class DecodificaResource(Resource):
    def post(self):
        miTokenJWT=request.json["token"]
        print(decode_token(miTokenJWT))
        payload=decode_token(miTokenJWT)
        payload['sub']=50
        print(payload)
        print(get_unverified_jwt_headers(miTokenJWT))
        print(miTokenJWT)

        header=get_unverified_jwt_headers(miTokenJWT)
        payload=decode_token(miTokenJWT)
        payload['sub']=50
        
        #base64Header = b64Encode(header)
        base64Header = base64_encode(header)
        base64Payload = base64_encode(payload)
        #signature = HMACSHA256(base64Header + '.' + base64Payload, app.config["JWT_SECRET_KEY"])
        #Token = base64Header + '.' + base64Payload + '.' + signature

        return miTokenJWT

class CreaResource(Resource):
    def get(self, id_usuario):
        access_token = create_access_token(identity=int(id_usuario))
        return jsonify(access_token=access_token)


api.add_resource(AuthResource, '/jwt')
api.add_resource(DecodificaResource, '/jwt/decodifica')
api.add_resource(CreaResource, '/jwt/creatoken/<int:id_usuario>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5006)