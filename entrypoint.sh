#!/bin/bash
set -e

# Lê secrets em runtime e seta envs (não vaza na imagem)
export SECRET_KEY=$(cat /run/secrets/secret_key)
export DATABASE_URL=$(cat /run/secrets/database_url)
export DB_USER=$(cat /run/secrets/db_user)
export DB_NAME=$(cat /run/secrets/db_name)
export DB_PASSWORD=$(cat /run/secrets/db_password)

# Aplica migrações Django (aguarda DB pronto)
echo "Aguardando banco de dados..."
until PGPASSWORD=DB_PASSWORD psql -h "bancodados" -U "${DB_USER:-postgres}" -d "${DB_NAME:-postgres}" -c '\q'; do
  >&2 echo "Banco de dados não está pronto - aguardando..."
  sleep 1
done

>&2 echo "Banco de dados pronto - aplicando migrações..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Inicia o servidor (ou o que o CMD definir)
exec "$@"