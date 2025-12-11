#!/bin/bash
set -e  # Para em erro (crítico para prod)

# Lê os secrets montados (cada .txt tem um valor por linha)
DB_USER=$(cat /run/secrets/db_user)
DB_NAME=$(cat /run/secrets/db_name)
DB_PASSWORD=$(cat /run/secrets/db_password)

# Valida: Se vazio, falha explicitamente (melhor que crash silencioso)
if [[ -z "$DB_USER" || -z "$DB_NAME" || -z "$DB_PASSWORD" ]]; then
    echo "Erro crítico: Secrets de banco vazios ou ausentes. Verifique arquivos .txt."
    exit 1
fi

# Exporta vars reais para o PostgreSQL (agora "meuuser", não path)
export POSTGRES_USER="$DB_USER"
export POSTGRES_DB="$DB_NAME"
export POSTGRES_PASSWORD="$DB_PASSWORD"

# Executa o entrypoint oficial do Postgres (inicia o banco com vars corretas)
exec docker-entrypoint.sh postgres