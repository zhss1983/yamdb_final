FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt /code
 #&&\
 #apt update &&\
 #apt -y upgrade
 #apt -y install snapd &&\
 #snap install core &&\
 #snap refresh core &&\
 #snap install --classic certbot &&\
 #ln -s /snap/bin/certbot /usr/bin/certbot

RUN pip install -r /code/requirements.txt

COPY . .

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
