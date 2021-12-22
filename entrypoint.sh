#!/bin/sh

while ! nc -z db 5432; do
  sleep 0.1
done

python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py loaddata init_admin.json --app customer
exec "$@"
