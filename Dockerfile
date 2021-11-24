FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt /code &&\
 sudo apt install snapd &&\
 sudo snap install core &&\
 sudo snap refresh core &&\
 sudo snap install --classic certbot &&\
 sudo ln -s /snap/bin/certbot /usr/bin/certbot

RUN pip install -r /code/requirements.txt

COPY . .

# CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
