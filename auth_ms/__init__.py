from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    app.config['FLASK_RUN_PORT'] = 5001
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

    #app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tutorialcanciones.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/db_abc'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['PROPAGATE_EXCEPTIONS'] = True

    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]

    return app