# Usa imagem slim estável
FROM python:3.12-slim

# Diretório de trabalho
WORKDIR /app

# Variáveis padrão
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# COPIA O ARQUIVO .env.build (somente para o build)
# Nunca copie .env real para a imagem
COPY .env.build /app/.env.build

# Carrega somente durante o build (para collectstatic)
RUN export $(grep -v '^#' /app/.env.build | xargs) && \
    rm /app/.env.build

RUM printenv

# Arquivo de dependências
COPY requirements.txt .

# Instala dependências Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Coleta arquivos estáticos usando variáveis carregadas
RUN python manage.py collectstatic --noinput

# Torna entrypoint executável
RUN chmod +x /app/entrypoint.sh

# Porta interna
EXPOSE 8000

# Inicia Gunicorn
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]