from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Zona(enum.Enum):
   RESIDENCIAL = 1
   COMERCIAL = 2
   INDUSTRIAL = 3
   BANCARIA = 4

class Ubicacion(db.Model):
    __tablename__ = 'ubicaciones'

    id = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String(80), nullable=False)
    zona = db.Column(db.Enum(Zona))
    id_usuario = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Ubicacion: {self.direccion}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Ubicacion.query.get(id)

    @staticmethod
    def get_by_usuario(id_usuario):
        return Ubicacion.query.filter_by(id_usuario=id_usuario).all()

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class UbicacionSchema(SQLAlchemyAutoSchema):
    zona = EnumADiccionario(attribute=("zona"))
    class Meta:
         model = Ubicacion
         include_relationships = True
         load_instance = True