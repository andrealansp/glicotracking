FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN --mount=type=secret,id=secret_key \
    --mount=type=secret,id=database_url

# Instala dependências do sistema (incluindo PostgreSQL client para migrações)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala pacotes Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Garante que entrypoint é executável (entrypoint.sh lerá secrets e setará envs)
RUN chmod +x /app/entrypoint.sh

# Entry point inicia o app após setup (migrações, etc.)
ENTRYPOINT ["/app/entrypoint.sh"]

# Coleta static files (pode ser movido para entrypoint se precisar de envs dinâmicas)
RUN python manage.py collectstatic --noinput

# Expõe a porta do Gunicorn
EXPOSE 8000

# Comando padrão: Gunicorn (pode ser sobrescrito no compose)
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]