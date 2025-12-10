FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema: PostgreSQL e gcc
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements.txt antes de instalar
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o projeto após a instalação
COPY . .

# Carrega .env.build de forma segura apenas durante o build para collectstatic
RUN set -a && . /app/.env.build && set +a

# Executa collectstatic sem necessidade de DB
RUN python manage.py collectstatic --noinput

# Torna entrypoint.sh executável
RUN chmod +x entrypoint.sh

# Expõe a porta 8000
EXPOSE 8000

# Inicia Gunicorn
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]