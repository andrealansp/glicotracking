# Use uma imagem base Python slim para menor tamanho (3.12 estável em vez de 3.15 alpha)
FROM python:3.12-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /glicotracking

# Variáveis de ambiente no formato moderno (evita warnings e melhora legibilidade)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema (otimizado para cache)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/

# Copia apenas requirements.txt primeiro (melhora cache em rebuilds)
COPY requirements.txt .

# Atualiza o PIP e instala dependências (sem cache para reduzir tamanho)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o resto do código (após instalação, para cache eficiente)
COPY . .

# Comando para coletar arquivos estáticos (assume settings configurados)
RUN python manage.py collectstatic --noinput

# Torna entrypoint executável
RUN chmod +x /glicotracking/entrypoint.sh


# Expose a porta que o Gunicorn vai escutar internamente
EXPOSE 8000

# Comando padrão para iniciar o Gunicorn (sintaxe corrigida: valores após flags)
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]