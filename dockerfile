FROM python:3

WORKDIR /usr/src/app

COPY . .
RUN pip install Flask
RUN pip install py7zr
CMD [ "python", "./app.py" ]