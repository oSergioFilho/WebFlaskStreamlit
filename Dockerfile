# Dockerfile
FROM python:3.11-slim
ARG SERVICE_DIR
WORKDIR /app

# Copia requirements e instala
COPY ${SERVICE_DIR}/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do serviço
COPY ${SERVICE_DIR} /app

# Expõe portas genéricas (backend 5000, frontend 8501)
EXPOSE 5000 8501