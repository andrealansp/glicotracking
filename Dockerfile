# Use uma imagem base Python slim para menor tamanho
FROM python:3.15.0a1-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /glicotracking

RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/

# Copia os arquivos
COPY . .

#  Atualiza o PIP
RUN pip install --upgrade pip

# Usa --no-cache-dir para evitar o armazenamento de cache pip e reduzir o tamanho da imagem
RUN pip install --no-cache-dir -r requirements.txt

# Comando para coletar arquivos estáticos
RUN python manage.py collectstatic --noinput


# Expose a porta que o Gunicorn vai escutar internamente
EXPOSE 8000

# Comando padrão para iniciar o Gunicorn (pode ser sobrescrito pelo docker-compose)
# Substitua 'myproject' pelo nome real do seu projeto Django
CMD ["gunicorn","app.wsgi:application","--bind","0.0.0.0:8000"]