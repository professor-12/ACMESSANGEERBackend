#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

cd src

chown $(whoami):$(whoami) db.sqlite3

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py runserver 0.0.0.0:8000
