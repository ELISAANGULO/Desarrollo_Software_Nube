from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from googleapiclient.discovery import build
from google.cloud import pubsub_v1
from google.oauth2 import service_account
from googleapiclient.discovery import build
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
        credentials = service_account.Credentials.from_service_account_file(
            'credSub.json')
        service = build('gmail', 'v1', credentials=credentials)
        project_id = "amazing-limiter-382016"
        topic_id = "DocumentToConvert"
        subscription_id = "DocumentToConvert-sub"
        # Number of seconds the subscriber should listen for messages
        timeout = 35000
        subscriber = pubsub_v1.SubscriberClient()
        # The `subscription_path` method creates a fully qualified identifier
        # in the form `projects/{project_id}/subscriptions/{subscription_id}`
        subscription_path = subscriber.subscription_path(project_id, subscription_id)

        def callback(body: pubsub_v1.subscriber.message.Message) -> None:
                try:
                    jsonString=str(body.data).replace('b"{', '{')
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
                    
                    conversion = session.query(Conversion).filter(
                        Conversion.nombre_archivo_convertido_gcp == nombre_archivo_convertido_gcp ).first()
                    
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
                body.ack()
        streaming_pull_future=subscriber.subscribe(
        subscription_path, callback = callback)
        print(f"Listening for messages on {subscription_path}..\n")
            # Wrap subscriber in a 'with' block to automatically call close() when done.
        with subscriber:
            try:
                 # When `timeout` is not set, result() will block indefinitely,
                # unless an exception is encountered first.
                streaming_pull_future.result(timeout = timeout)
            except TimeoutError:
                streaming_pull_future.cancel()  # Trigger the shutdown.
                # Block until the shutdown is complete.
                streaming_pull_future.result()
