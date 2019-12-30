#!/bin/bash
set -e
cd /site

pip install service_identity

mv /kindlegen/kindlegen /site/kmanga/bin

echo "BEFORE MIGRATIONS"
kmanga/manage.py makemigrations

cp bin/0002_full_text_search.py kmanga/core/migrations/
kmanga/manage.py migrate
kmanga/manage.py loaddata bin/initialdata.json

echo "AFTER MIGRATIONS"
exec "$@"
