import pika
import json
import base64
from models import Base, engine
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import numpy as np
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text,ForeignKey,Date, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from Listener import GcpCloudStorage
from .Archivo import Archivo
from models.modelos import Conversion, Session

class ListenerServicioConsulta():
    def __init__(self):
      print("Constructor")

    def listenerConsultaVentas(self):
      print("listenerConsultaVentas")
      parameters = pika.ConnectionParameters(
          '34.138.120.16', 5672, '/', pika.PlainCredentials(username='admin', password='admin'), heartbeat=0)
      connection = pika.BlockingConnection(parameters)
      
      channel = connection.channel()

      #channel.exchange_declare(exchange='', exchange_type='fanout')

      result = channel.queue_declare(queue='DocumentToConvert', exclusive=False)
      queue_name = result.method.queue

      #channel.queue_bind(exchange='logs', queue=queue_name)

   


      def callback(ch, method, properties, body):
          try:
              jsonString = str(body).replace('b"{','{')
              jsonString = jsonString.replace('}"','}')
              jsonString = jsonString.replace("'", '"')
              aDict = json.loads(jsonString)
              #engine = create_engine('postgresql://postgres:postgres@localhost:5432/conversor')
              db_uri = 'postgresql://postgres:andes@35.196.5.117:5432/conversor'
              engine = create_engine(db_uri)

              Session = sessionmaker(bind=engine)
              session = Session()
              nombre_archivo_original_gcp = aDict["nombre_archivo_original_gcp"]
              nombre_archivo_convertido_gcp = aDict["nombre_archivo_convertido_gcp"]
              
            #   conversion = session.query(Conversion).filter(
            #       Conversion.nombre_archivo_convertido_gcp == nombre_archivo_convertido_gcp ).first()
              print("###########"+nombre_archivo_convertido_gcp)
              conversion = session.query(Conversion).filter(Conversion.nombre_archivo_convertido_gcp == nombre_archivo_convertido_gcp).first()
              #conversion = Conversion.query.filter_by(nombre_archivo_convertido_gcp=nombre_archivo_convertido_gcp).first()
              base64_archivo_original = conversion.archivo_base64_original
              archivo_bytes = base64.b64decode(base64_archivo_original)
              formato_destino = conversion.extension_destino

              with open(nombre_archivo_original_gcp, 'wb') as f:
                f.write(np.array(archivo_bytes))

              archivo = Archivo(nombre_archivo_original_gcp)
              nuevoArchivo=""
              if (formato_destino == "pdf"):  
                    nuevoArchivo=archivo.comprimir_a_tar_gz(nombre_archivo_original_gcp,nombre_archivo_convertido_gcp)
              elif (formato_destino == "tar.gz"):
                    nuevoArchivo=archivo.comprimir_a_tar_gz(nombre_archivo_original_gcp,nombre_archivo_convertido_gcp)
              elif (formato_destino == "zip"):
                    nuevoArchivo=archivo.comprimir_a_zip(nombre_archivo_original_gcp,nombre_archivo_convertido_gcp)
              elif (formato_destino == "7z"):
                    nuevoArchivo=archivo.comprimir_a_7z(nombre_archivo_original_gcp,nombre_archivo_convertido_gcp)
              
             
              GcpCloudStorage.upload_to_bucket(
                  nombre_archivo_convertido_gcp, nombre_archivo_convertido_gcp, "Convertidos/")
              GcpCloudStorage.upload_to_bucket(
                  nombre_archivo_original_gcp, nombre_archivo_original_gcp, "Originales/")
              conversion.disponible = True
              #conversion.archivo__base64_convertido = nuevoArchivo
              conversion.status= 'processed'
              session.commit()
              session.close()
              os.remove(nombre_archivo_convertido_gcp)
              os.remove(nombre_archivo_original_gcp)
          except Exception as e:
            print("Se presentó el siguiente error", e)
          

      channel.basic_consume(
          queue=queue_name, on_message_callback=callback, auto_ack=True)

      channel.start_consuming()
