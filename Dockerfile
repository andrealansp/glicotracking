FROM python:3.13.5-slim
LABEL authors="a.alves"
WORKDIR /app
RUN apt-get update && apt-get install -y curl
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
