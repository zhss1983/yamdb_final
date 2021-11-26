#!/bin/bash

sudo docker exec sergey_web_1 python manage.py collectstatic
sudo docker exec sergey_web_1 python manage.py migrate
sudo docker exec sergey_web_1 python manage.py loaddata fixtures.json