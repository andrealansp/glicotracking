#!/bin/bash
set -e  # Para em erro

echo "=== DEBUG: Iniciando entrypoint.sh ==="

# Lê paths dos secrets via env vars do compose (minúsculas)
SECRET_KEY_PATH="${secret_key:-/run/secrets/secret_key}"
DB_NAME_PATH="${db_name:-/run/secrets/db_name}"
DB_PASSWORD_PATH="${db_password:-/run/secrets/db_password}"
DB_USER_PATH="${db_user:-/run/secrets/db_user}"
DATABASE_URL_PATH="${database_url:-/run/secrets/database_url}"

echo "=== DEBUG: Paths lidos - SECRET_KEY_PATH: $SECRET_KEY_PATH ==="

# Exporta valores reais (cat lê o arquivo secret)
export SECRET_KEY=$(cat "$SECRET_KEY_PATH" 2>/dev/null || echo "ERRO: Secret não encontrado")
export DB_NAME=$(cat "$DB_NAME_PATH" 2>/dev/null || echo "ERRO: Secret não encontrado")
export DB_PASSWORD=$(cat "$DB_PASSWORD_PATH" 2>/dev/null || echo "ERRO: Secret não encontrado")
export DB_USER=$(cat "$DB_USER_PATH" 2>/dev/null || echo "ERRO: Secret não encontrado")

# DEBUG: Log valores (sem sensíveis reais – só status)
echo "=== DEBUG: Valores lidos - SECRET_KEY: ${SECRET_KEY:0:10}... (comprimento: ${#SECRET_KEY}) ==="
echo "=== DEBUG: DB_USER: $DB_USER (deve ser nome real, não path) ==="

# Constrói DATABASE_URL: Prioriza arquivo dedicado, senão monta
if [[ -f "$DATABASE_URL_PATH" ]]; then
    export DATABASE_URL=$(cat "$DATABASE_URL_PATH" 2>/dev/null || echo "ERRO: Arquivo não lido")
    echo "=== DEBUG: DATABASE_URL de arquivo dedicado: ${DATABASE_URL:0:20}... (comprimento: ${#DATABASE_URL}) ==="
else
    # Monta com partes (use host 'bancodados' para DNS Docker)
    if [[ "$DB_USER" != "ERRO"* && "$DB_PASSWORD" != "ERRO"* && "$DB_NAME" != "ERRO"* ]]; then
        export DATABASE_URL="postgres://${DB_USER}:${DB_PASSWORD}@bancodados:5432/${DB_NAME}"
        echo "=== DEBUG: DATABASE_URL montada dinamicamente: $DATABASE_URL ==="
    else
        export DATABASE_URL="ERRO: Falha na montagem"
        echo "=== ERRO: Não foi possível montar DATABASE_URL ==="
        exit 1
    fi
fi

# Valida vars críticas (SECRET_KEY e DATABASE_URL)
if [[ "$SECRET_KEY" == "ERRO"* || "$DATABASE_URL" == "ERRO"* ]]; then
    echo "=== ERRO CRÍTICO: SECRET_KEY ou DATABASE_URL inválidos. Verifique secrets no Portainer. ==="
    exit 1
fi

echo "=== DEBUG: Todas vars válidas. Iniciando setup Django ==="

# Setup Django (agora com vars exportadas)
python manage.py migrate --noinput || echo "=== AVISO: Migrações falharam (DB não pronto?) ==="
python manage.py collectstatic --noinput || echo "=== AVISO: Collectstatic falhou ==="

echo "=== DEBUG: Setup completo. Iniciando Gunicorn ==="
exec "$@"  # Executa o command do compose (Gunicorn herda as exports)