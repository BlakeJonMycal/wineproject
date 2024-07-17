#!/bin/bash

rm db.sqlite3
rm -rf ./wineapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations wineapi
python3 manage.py migrate wineapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

