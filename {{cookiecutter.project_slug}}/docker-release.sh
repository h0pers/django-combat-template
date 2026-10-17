#!/bin/sh
# vim:sw=4:ts=4:et
set -e

su-exec "$USER" python manage.py migrate --noinput
su-exec "$USER" python manage.py collectstatic --noinput

NO_USERS="from django.contrib.auth import get_user_model; User = get_user_model(); exit(User.objects.exists())"
if su-exec "$USER" python manage.py shell -c "$NO_USERS"; then
  su-exec "$USER" python manage.py createsuperuser --noinput
fi
