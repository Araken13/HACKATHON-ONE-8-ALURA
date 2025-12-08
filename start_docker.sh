#!/bin/bash

echo "🐳 Iniciando infraestrutura CHURN via Docker..."

# Derrubar containers antigos se houver
docker compose down

# Limpar porta 8000 se tiver algo rodando (opcional, requer sudo as vezes)
# fuser -k 8000/tcp 

# Build e Up
echo "🛠️ Construindo imagens..."
docker compose up -d --build

echo "✅ Containers Online!"
echo "-----------------------------------"
echo "📊 Grafana: http://localhost:3000 (admin/admin)"
echo "📡 API:     http://localhost:8000"
echo "💾 Banco:   localhost:5432"
echo "sw"
docker compose ps
