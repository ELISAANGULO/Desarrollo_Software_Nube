import os
import py7zr
import tarfile
#import aspose.words as aw
import zipfile
import base64
class Archivo:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.nuevoArchivo=""

    def comprimir_a_tar_gz(self, nombre_archivo_tar_gz):
        """
        Comprime un archivo en formato tar.gz con un nombre especificado.
        :param nombre_archivo_tar_gz: Nombre del archivo tar.gz de salida.
        :type nombre_archivo_tar_gz: str
        """
        with tarfile.open(nombre_archivo_tar_gz, mode="w:gz") as archivo_tar_gz:
            archivo_tar_gz.add(self.ruta_archivo)
        print(f'Se ha creado el archivo tar.gz: {nombre_archivo_tar_gz}')
        self.nuevoArchivo = nombre_archivo_tar_gz
        return self.convertString64()

    def comprimir_a_zip(self, nombre_archivo_zip):
        """
        Comprime un archivo en formato zip con un nombre especificado.
        :param nombre_archivo_zip: Nombre del archivo zip de salida.
        :type nombre_archivo_zip: str
        """
        with zipfile.ZipFile(nombre_archivo_zip, 'w') as f:
            f.write(self.ruta_archivo)
        print(f'Se ha creado el archivo zip: {nombre_archivo_zip}')
        self.nuevoArchivo = nombre_archivo_zip
        return self.convertString64()

    def convertString64(self):
        print(self.nuevoArchivo)
        # Abrir el archivo y leer su contenido en un objeto de bytes
        with open(self.nuevoArchivo, 'rb') as archivo:
            contenido = archivo.read()
        # Codificar el objeto de bytes en base64
        contenido_codificado = base64.b64encode(contenido)
        # Decodificar el objeto de bytes codificado en una cadena
        contenido_en_base64 = contenido_codificado.decode('utf-8')
        return contenido_en_base64
