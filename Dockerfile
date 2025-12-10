FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    vim \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --noinput

# ---------- SOMENTE VARIÁVEIS NECESSÁRIAS PARA O BUILD ----------
COPY .env.build /app/.env.build

# Carrega apenas SECRET_KEY e DEBUG para o build
RUN export $(grep -v '^#' /app/.env.build | grep -E '^(SECRET_KEY|DEBUG)=' | xargs) && \
    rm /app/.env.build &&  \

# Copia código
COPY . .

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]