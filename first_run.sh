#!/bin/bash

sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic
sudo docker-compose exec web python manage.py loaddata fixtures.json
