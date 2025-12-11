#!/bin/bash

# Aplica migrações Django (aguarda DB pronto)
echo "Aguardando banco de dados..."
until PGPASSWORD=$DB_PASSWORD_GTK psql -h "bancodados" -U "${DB_USER:-postgres}" -d "${DB_NAME_GTK:-postgres}" -c '\q'; do
  >&2 echo "Banco de dados não está pronto - aguardando..."
  sleep 1
done

>&2 echo "Banco de dados pronto - aplicando migrações..."
python manage.py migrate --noinput

# Inicia o servidor (ou o que o CMD definir)
exec "$@"