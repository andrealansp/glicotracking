#!/bin/bash
set -e  # Para em erro (crítico para prod)

# Valida: Se vazio, falha explicitamente (melhor que crash silencioso)
if [[ -z "$db_use" || -z "$db_name" || -z "$db_password" ]]; then
    echo "Erro crítico: Secrets de banco vazios ou ausentes. Verifique arquivos .txt."
    exit 1
fi

# Exporta vars reais para o PostgreSQL (agora "meuuser", não path)
export POSTGRES_USER="$DB_USER"
export POSTGRES_DB="$DB_NAME"
export POSTGRES_PASSWORD="$DB_PASSWORD"

# Executa o entrypoint oficial do Postgres (inicia o banco com vars corretas)
exec docker-entrypoint.sh postgres