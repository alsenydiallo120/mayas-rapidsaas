#!/bin/sh

echo 'Running migrations...'
python src/manage.py migrate
echo 'Compressing static files...'
python src/manage.py compress --force
echo 'Collecting static files...'
python src/manage.py collectstatic --noinput --clear --no-post-process
echo 'Generating proxy config file...'
python src/manage.py generate_proxy_config

cd /code/src
exec "$@"