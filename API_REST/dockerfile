FROM python:3

WORKDIR /usr/src/app

COPY . .
RUN pip install Flask
RUN pip install py7zr
RUN pip install flask_sqlalchemy
RUN pip install marshmallow_sqlalchemy
RUN pip install sqlalchemy
RUN pip install flask_cors
RUN pip install psycopg2
RUN pip install flask_restful
RUN pip install flask_jwt_extended
CMD [ "python", "./app.py" ]