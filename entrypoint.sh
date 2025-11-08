#!/bin/sh
set -e

echo "🌍 Ambiente atual: $ENVIRONMENT"

if [ "$ENVIRONMENT" = "prod" ]; then
  echo "📦 Coletando arquivos estáticos..."
  python manage.py collectstatic --noinput

  echo "🚀 Iniciando Gunicorn..."
  exec gunicorn app.wsgi:application --bind 0.0.0.0:8000

else
  echo "📚 Rodando migrações..."
  python manage.py makemigrations
  python manage.py migrate

  echo "💻 Iniciando servidor de desenvolvimento..."
  exec python manage.py runserver 0.0.0.0:8000
fi
