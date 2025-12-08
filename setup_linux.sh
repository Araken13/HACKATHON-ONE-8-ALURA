#!/bin/bash

echo "🐧 Configurando ambiente Linux para OCI/WSL..."

# 1. Garantir que o módulo venv do sistema está instalado
# (Às vezes o Python vem instalado, mas o gerador de venv não)
echo "📦 Instalando dependências do sistema..."
sudo apt-get update && sudo apt-get install -y python3-venv python3-full python3-pip

# 2. Limpar ambiente antigo viciado
if [ -d "venv" ]; then
    echo "🧹 Removendo venv antigo..."
    rm -rf venv
fi

# 3. Criar novo ambiente virtual limpo
echo "🔨 Criando novo ambiente virtual (venv)..."
python3 -m venv venv

# 4. Instalar as bibliotecas DENTRO do venv
echo "⬇️ Instalando bibliotecas do requirements.txt..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# 5. Criar arquivo de execução rápida
echo "#!/bin/bash
export DATABASE_URL='postgresql://user:password@localhost:5432/churn_db'
./venv/bin/uvicorn api:app --host 0.0.0.0 --port 8000 --reload
" > run_api.sh
chmod +x run_api.sh

echo "✅ AMBIENTE PRONTO!"
echo "---------------------------------------------------"
echo "Para rodar a API agora e sempre, execute:"
echo "./run_api.sh"
echo "---------------------------------------------------"
