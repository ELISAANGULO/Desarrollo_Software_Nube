from marshmallow import fields, Schema
from sqlalchemy import  Column, Integer, String, Boolean, Text,ForeignKey,Date, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Conexión a la base de datos
db_uri = 'postgresql://postgres:andes@35.196.5.117:5432/conversor'
engine = create_engine(db_uri)
#engine = create_engine('postgresql://postgres:postgres@localhost:5432/conversor')
Base = declarative_base()
Session = sessionmaker(bind=engine)


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
    nombre_archivo_original = Column(String)
    nombre_archivo_original_gcp = Column(String)
    nombre_archivo_convertido_gcp = Column(String)
    archivo_base64_original = Column(Text)
    archivo__base64_convertido = Column(Text)
    extension_original = Column(String)
    extension_destino = Column(String)
    disponible = Column(Boolean)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    fecha_subida = Column(DateTime)
    fecha_modificacion = Column(DateTime)
    status = Column(String)

class UsuarioSchema(Schema):
    id = Column(Integer, primary_key=True)
    usuario = fields.Str()
    correo = fields.Str()

class ConversionSchema(Schema):
    id = fields.Integer()
    nombre_archivo_original = fields.Str()
    nombre_archivo_original_gcp = fields.Str()
    nombre_archivo_convertido_gcp = fields.Str()
    archivo_base64_original = fields.Str()
    archivo__base64_convertido = fields.Str()
    extension_original = fields.Str()
    extension_destino = fields.Str()
    fecha_subida = fields.Str()
    fecha_modificacion = fields.Str()
    status = fields.Str()
    disponible = fields.Boolean()
    usuario_id = fields.Integer()
    usuario = fields.Nested(UsuarioSchema)


