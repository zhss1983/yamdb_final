FROM python:3.9-slim

RUN mkdir /code

WORKDIR /code

#VOLUME /code

COPY requirements.txt /code

RUN pip install -r /code/requirements.txt

COPY . .

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
