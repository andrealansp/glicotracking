#!/bin/bash
set -e  # Para em erro

# Setup Django (agora com vars exportadas)
python manage.py migrate --noinput || echo "=== AVISO: Migrações falharam (DB não pronto?) ==="
python manage.py collectstatic --noinput || echo "=== AVISO: Collectstatic falhou ==="


exec "$@"  # Executa o command do compose (Gunicorn herda as exports)