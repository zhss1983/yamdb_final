#!/bin/bash

cp -r ./data/static ./data/static_backup
rm -rf ./data/static
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py loaddata fixtures.json
echo "include /data/nginx/default_first.conf;" > ./nginx/default.conf
chmod 766 ./nginx/default.conf
docker-compose restart
./init-letsencrypt.sh
echo "include /data/nginx/default_evryday.conf;" > ./nginx/default.conf
chmod 766 ./nginx/default.conf
docker-compose restart
