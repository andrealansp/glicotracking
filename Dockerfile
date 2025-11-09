# Use uma imagem base Python slim para menor tamanho
FROM python:3.15-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
# Usa --no-cache-dir para evitar o armazenamento de cache pip e reduzir o tamanho da imagem
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Comando para coletar arquivos estáticos
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Copia o restante do código da aplicação para o diretório de trabalho
# Certifique-se de que sua aplicação Django (incluindo manage.py e o diretório do projeto) esteja na pasta 'app' no host
COPY app/ .

# Expose a porta que o Gunicorn vai escutar internamente
EXPOSE 8000



# Comando padrão para iniciar o Gunicorn (pode ser sobrescrito pelo docker-compose)
# Substitua 'myproject' pelo nome real do seu projeto Django
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]