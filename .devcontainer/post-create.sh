#!/usr/bin/env bash
set -euo pipefail

cd /workspace/thscoreboard

configure_git_signing() {
  local global_sign local_sign fallback signing_key

  global_sign="$(git config --global --bool --get commit.gpgsign || true)"
  local_sign="$(git config --local --bool --get commit.gpgsign || true)"
  fallback="$(git config --local --bool --get devcontainer.gpgsignFallback || true)"

  if [[ "${global_sign}" != "true" && "${local_sign}" != "true" && "${fallback}" != "true" ]]; then
    return
  fi

  if ! command -v gpg >/dev/null 2>&1; then
    git config --local commit.gpgsign false
    git config --local devcontainer.gpgsignFallback true
    return
  fi

  signing_key="$(git config --global --get user.signingkey || git config --get user.signingkey || true)"
  if [[ -n "${signing_key}" ]]; then
    if gpg --batch --list-secret-keys "${signing_key}" >/dev/null 2>&1; then
      if [[ "${fallback}" == "true" ]]; then
        git config --local --unset commit.gpgsign >/dev/null 2>&1 || true
        git config --local --unset devcontainer.gpgsignFallback >/dev/null 2>&1 || true
      fi
    else
      git config --local commit.gpgsign false
      git config --local devcontainer.gpgsignFallback true
    fi
    return
  fi

  if gpg --batch --list-secret-keys --with-colons 2>/dev/null | grep -q '^sec'; then
    if [[ "${fallback}" == "true" ]]; then
      git config --local --unset commit.gpgsign >/dev/null 2>&1 || true
      git config --local --unset devcontainer.gpgsignFallback >/dev/null 2>&1 || true
    fi
  else
    git config --local commit.gpgsign false
    git config --local devcontainer.gpgsignFallback true
  fi
}

configure_git_signing

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
