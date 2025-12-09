#!/bin/bash

# Define o diretório de destino na home do usuário Linux (onde a performance é 10x maior)
TARGET_DIR=~/churn-insight-wsl

echo "🚀 Iniciando migração para o sistema de arquivos Linux..."
echo "📂 Origem: $(pwd)"
echo "📂 Destino: $TARGET_DIR"

# Criar pasta
mkdir -p "$TARGET_DIR"

# Verificar se rsync está instalado
if command -v rsync >/dev/null 2>&1; then
    echo "📦 Copiando arquivos (ignorando lixo: node_modules, venv, git)..."
    rsync -av --progress . "$TARGET_DIR" \
        --exclude 'node_modules' \
        --exclude '.venv' \
        --exclude 'venv' \
        --exclude '.git' \
        --exclude '__pycache__' \
        --exclude 'dist' \
        --exclude '.pytest_cache' \
        --exclude 'churn_database.db' \
        --exclude 'postgres_data'
else
    echo "⚠️ 'rsync' não encontrado. Usando 'cp' normal."
    echo "⚠️ Isso vai copiar node_modules e venv incorretos, que apaharemos em seguida..."
    cp -r . "$TARGET_DIR"
    
    echo "🧹 Limpando binários Windows incompatíveis..."
    rm -rf "$TARGET_DIR/node_modules"
    rm -rf "$TARGET_DIR/venv"
    rm -rf "$TARGET_DIR/.venv"
    rm -rf "$TARGET_DIR/.git"
fi

echo ""
echo "✅ Migração concluída com sucesso!"
echo "-----------------------------------------------------------"
echo "👣 PRÓXIMOS PASSOS:"
echo "1. No seu terminal WSL, entre na pasta:"
echo "   cd $TARGET_DIR"
echo ""
echo "2. Abra o VS Code nesta nova pasta:"
echo "   code ."
echo ""
echo "3. Reinstale as dependências (já que não copiamos as do Windows):"
echo "   ./setup_linux.sh"
echo "   cd frontend && npm install"
echo "-----------------------------------------------------------"
