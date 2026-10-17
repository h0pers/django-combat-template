#!/bin/sh
# vim:sw=4:ts=4:et

if [ "$1" = "--debug" ]; then
  /docker-release.sh
  # Django development server
  exec su-exec "$USER" python manage.py runserver "0.0.0.0:8000"
else
  # Gunicorn
  exec su-exec "$USER" gunicorn -c gunicorn.conf.py "$PROJECT_NAME.wsgi:application"
fi
