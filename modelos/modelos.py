from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text,ForeignKey,Date, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Conexión a la base de datos
db_uri = 'postgresql://postgres:andes@35.196.5.117:5432/conversor'
engine = create_engine(db_uri)
#engine = create_engine('postgresql://postgres:postgres@localhost:5432/conversor')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    usuario = Column(String(50))
    contrasena = Column(String(50))
    correo = Column(String(50))
    conversiones = relationship('Conversion', backref='usuario')

class Conversion(Base):
    __tablename__ = 'conversiones'
    id = Column(Integer, primary_key=True)
    nombre_archivo = Column(String)
    archivo_base = Column(Text)
    extension_original = Column(String)
    archivo_convertido = Column(Text)
    extension_destino = Column(String)
    disponible = Column(Boolean)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    fecha_subida = Column(DateTime)
    status = Column(String)

class UsuarioSchema(Schema):
    id = Column(Integer, primary_key=True)
    usuario = fields.Str()
    correo = fields.Str()

class ConversionSchema(Schema):
    id = fields.Integer()
    nombre_archivo = fields.Str()
    archivo_base = fields.Str()
    extension_original = fields.Str()
    archivo_convertido = fields.Str()
    extension_destino = fields.Str()
    fecha_subida = fields.Str()
    status = fields.Str()
    disponible = fields.Boolean()
    usuario_id = fields.Integer()
    usuario = fields.Nested(UsuarioSchema)


