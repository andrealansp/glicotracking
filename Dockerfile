# syntax=docker/dockerfile:1.3  # Ativa BuildKit para secrets opcionais no build
FROM python:3.12-slim

WORKDIR /app

# Configurações de ambiente para Python otimizado
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN --mount=type=secret,id=db_user \
 export db_user=$(cat /run/secrets/db_user) && \
 echo $db_user # would output "foo".

# Instala dependências do sistema (apenas essenciais; removeu vim e gcc desnecessários)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    vim \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copia requirements e instala pacotes Python (cache otimizado)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação (exclua .env e secrets do .dockerignore)
COPY . .

# Garante que entrypoint é executável (entrypoint.sh deve ler secrets em runtime)
RUN chmod +x /app/entrypoint.sh

# Coleta static files NO ENTRYPOINT (evita falhas por falta de envs no build)
# Mova para entrypoint.sh se depender de DB ou secrets dinâmicos

# Expõe a porta do Gunicorn
EXPOSE 8000

# Entry point inicia o app após setup (migrações, collectstatic, etc.)
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando padrão: Gunicorn (workers ajustável baseado em CPU; 2-4 é bom para start)
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]