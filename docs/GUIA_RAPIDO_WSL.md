# 🐧 Guia Rápido: Executando no WSL

Este guia contém o passo a passo exato para rodar e validar o projeto **ChurnInsight** dentro do WSL (Windows Subsystem for Linux).

## 📋 Pré-requisitos

1. **Docker Desktop** rodando no Windows (com integração WSL 2 ativada em Settings > Resources > WSL Integration).
2. Terminal WSL aberto na pasta do projeto (`cd /mnt/d/HACKTHON1`).

---

## 🚀 Passo 1: Subir Banco de Dados e Grafana (Docker)

Antes de rodar a API Python, precisamos que o PostgreSQL esteja online. Vamos usar o Docker para isso, mas manter a API rodando localmente no Linux para fácil debug.

```bash
# Sobe apenas o banco (db) e o grafana em background (-d)
docker compose up -d db grafana
```

> **Verifique se subiu:**
> `docker compose ps`
> *Deve mostrar 'churn_db' e 'churn_grafana' como 'Up'.*

---

## 🐍 Passo 2: Configurar Ambiente Python (Backend)

Vamos configurar o ambiente virtual e instalar as dependências no Linux.

```bash
# Dá permissão de execução ao script de setup
chmod +x setup_linux.sh

# Executa o setup (cria venv e instala libs)
./setup_linux.sh
```

---

## ▶️ Passo 3: Rodar a API

O script de setup criou um atalho `run_api.sh` configurado para conectar no Postgres local.

```bash
# Dá permissão ao script de execução
chmod +x run_api.sh

# Roda a API (bloqueia o terminal mostrando logs)
./run_api.sh
```

*A API agora está acessível em `http://localhost:8000`.*

---

## 🎨 Passo 4: Rodar o Frontend

Abra uma **nova aba** no terminal WSL e navegue para a pasta do frontend.

```bash
cd /mnt/d/HACKTHON1/frontend

# Instala dependências (se ainda não fez)
npm install

# Roda o servidor de desenvolvimento
npm run dev
```

*O Frontend agora está acessível em `http://localhost:5173` (ou porta similar indicada).*

---

## 🧪 Passo 5: Testes e Validação

Para garantir que tudo está funcionando, você pode rodar os testes automatizados.

Em uma **terceira aba** (ou parando a API):

```bash
# Ativa o ambiente virtual
source venv/bin/activate

# Roda o teste End-to-End completo
python test_e2e_full.py
```

### ✅ Checklist de Sucesso

- [ ] API conecta no Banco sem erros.
- [ ] Frontend carrega e faz previsões.
- [ ] Grafana acessível em `http://localhost:3000` (admin/admin).
