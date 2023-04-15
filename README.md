# Desarrollo_Software_Nube
Repositorio para la asignatura de Cloud

Aplicacion realizada en python para ejecutar tenga en cuenta las instalaciones para probarla 

*pip install Flask

*pip install py7zr

*pip install flask_sqlalchemy

*pip install marshmallow_sqlalchemy

*pip install sqlalchemy

*pip install flask_cors

*pip install psycopg2

*pip install flask_restful

*pip install flask_jwt_extended


Esta aplicacion esta diseñada para correr exclusivamente en docker para esto ubiquese en la carpeta del proyecto y corra el comando

docker-compose up --build


Despues revisa que los contenedores se deberian ver a si corriendo

![imagen](https://user-images.githubusercontent.com/111519973/232250534-f71f05df-85f9-46ad-bf96-8fa89edf54c8.png)





Despues de realizar  este proceso podra ver la documentacion de los servicios en esta URL


https://documenter.getpostman.com/view/14097063/2s93XyShgP

![imagen](https://user-images.githubusercontent.com/111519973/232250609-63f3f704-7730-480b-b866-cd90aac9e1a2.png)


Ahora primero cree un usuario para esto llame el metodo sign in 
![imagen](https://user-images.githubusercontent.com/111519973/232250676-97b52f34-0b70-4d94-9b86-201f814cd396.png)


Este le informara si el usuario ya fue creado o no


# Obtencion de token

Llame el metodo login  con este obtendra el token 

![imagen](https://user-images.githubusercontent.com/111519973/232250743-2db41bd5-5d6a-467d-8c90-2ae31e74372a.png)


# Probar la herramienta con Apache Benchmark
 

El proyecto suministrado  tiene un json de prueba llamado fileTestPDF.json
![imagen](https://user-images.githubusercontent.com/111519973/232250872-c81ecccf-a12e-42f0-97f8-076af9895885.png)

Con power shell Ubicate  en la ruta donde se encuentra  el archivo despues se ejecutara el comando de prueba: 

 ab -n 1000 -c 500  -H "Accept: application/json" -H "Accept: application/json" -H "Authorization: Bearer <Mi token>" "http://127.0.0.1:5000/api/tasks"
 
 
 La prueba se veria asi en power shell
 
 ![imagen](https://user-images.githubusercontent.com/111519973/232250949-546259e2-c5ed-49d2-b134-c8be648964f1.png)






