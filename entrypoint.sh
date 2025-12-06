#!/bin/bash
set -e  # Para em erro (crítico para falha rápida)

# Espera DB pronto (se não, migrate falha)
echo "Aguardando banco de dados..."
until python manage.py dbshell >/dev/null 2>&1; do
    echo "DB ainda não pronto, aguardando 2s..."
    sleep 2
done
echo "DB pronto!"

# Roda migrações (e collectstatic se staticfiles em INSTALLED_APPS)
echo "Rodando migrações..."
python manage.py migrate --noinput

# Opcional: Collectstatic (se não no Dockerfile)
# python manage.py collectstatic --noinput

# Inicia Gunicorn (usa command do compose)
echo "Iniciando Gunicorn..."
exec "$@"