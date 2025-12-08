# Usar imagem leve do Python
FROM python:3.10-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias para compilar pacotes (se precisar)
# libpq-dev é necessário para o driver do Postgres (psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas arquivos de requisitos primeiro (cache layer)
# Copiar requirements primeiro para aproveitar cache do Docker
COPY requirements.txt .

# Instalar dependências a partir do arquivo
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código
COPY . .

# Expor a porta da API
EXPOSE 8000

# Comando de inicialização
CMD ["python", "api.py"]
