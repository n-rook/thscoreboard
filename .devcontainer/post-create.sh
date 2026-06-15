#!/usr/bin/env bash
set -euo pipefail

cd /workspace/thscoreboard

pip install --require-hashes -r requirements-dev.txt

cd /workspace/thscoreboard/project/thscoreboard
python manage.py migrate
python manage.py setup_constant_tables
python manage.py compilemessages

python manage.py shell -c "
import os
from django.contrib.auth import get_user_model

username = os.environ['DJANGO_SUPERUSER_USERNAME']
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
password = os.environ['DJANGO_SUPERUSER_PASSWORD']

User = get_user_model()

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )
"

npm ci
