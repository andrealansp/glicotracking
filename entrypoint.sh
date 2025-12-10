#!/bin/bash

# Lê secrets de /run/secrets/ e exporta como envs (substitui .env.build)
if [ -f /run/secrets/gtk_secret_key ]; then
    export GTK_SECRET_KEY=$(cat /run/secrets/gtk_secret_key)
fi

if [ -f /run/secrets/db_password_gtk ]; then
    export DB_PASSWORD_GTK=$(cat /run/secrets/db_password_gtk)
fi

if [ -f /run/secrets/db_name_gtk ]; then
    export DB_NAME_GTK=$(cat /run/secrets/db_name_gtk)
fi

if [ -f /run/secrets/database_url_gtk ]; then
    export DATABASE_URL_GTK=$(cat /run/secrets/database_url_gtk)
fi

# Monta DATABASE_URL usando as secrets (exemplo: se não usar a URL completa)
# Se DATABASE_URL_GTK for a URL full, use diretamente; senão, construa aqui
if [ -z "$DATABASE_URL_GTK" ] && [ -n "$DB_NAME_GTK" ] && [ -n "$DB_PASSWORD_GTK" ]; then
    export DATABASE_URL="postgresql://${DB_USER:-postgres}:${DB_PASSWORD_GTK}@bancodados:5432/${DB_NAME_GTK}"
else
    export DATABASE_URL="$DATABASE_URL_GTK"
fi

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