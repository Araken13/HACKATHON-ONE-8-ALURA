# 🛠️ Manual de Instalação Definitivo - ChurnInsight

Este guia fornece o passo a passo exato e validado para instalar e rodar o projeto **ChurnInsight** do zero. Se você seguir estes passos, **o projeto vai funcionar**.

---

## ✅ Pré-requisitos Obrigatórios

Antes de começar, certifique-se de ter instalado:

1. **Python** (3.10 ou superior) - [Baixar aqui](https://www.python.org/downloads/)
    * *Importante no Windows:* Marque a caixa "Add Python to PATH" na instalação.
2. **Node.js** (v18 ou superior) - [Baixar aqui](https://nodejs.org/)
3. **Git** - [Baixar aqui](https://git-scm.com/)

---

## 🖥️ Opção 1: Instalação no Windows (PowerShell)

### 1. Clonar ou Baixar o Projeto

Abra o **PowerShell** e navegue até a pasta onde deseja instalar.

```powershell
# Se você já tem a pasta, apenas entre nela:
cd D:\HACKTHON1
```

### 2. Configurar o Backend (API)

Vamos criar um ambiente virtual para isolar as dependências e evitar erros.

```powershell
# 1. Criar o ambiente virtual
python -m venv venv

# 2. Ativar o ambiente virtual
.\venv\Scripts\Activate

# 3. Instalar as dependências (backend)
pip install -r requirements.txt

# 4. Treinar o modelo de IA (Crucial!)
python train_model.py
# Saída esperada: "Pipeline finalizado com sucesso."

# 5. Iniciar o servidor da API
python api.py
```

> **Atenção:** Deixe este terminal aberto rodando a API. Não o feche.

### 3. Configurar o Frontend (Site)

Abra um **NOVO** terminal PowerShell (mantenha o anterior aberto).

```powershell
# 1. Entrar na pasta do projeto e depois na pasta frontend
cd D:\HACKTHON1
cd frontend

# 2. Instalar dependências do site
npm install

# 3. Iniciar o site
npm run dev
```

### 4. Usar

Acesse no seu navegador: **<http://localhost:5173>** (ou a porta que aparecer no terminal).

---

## 🐧 Opção 2: Instalação no Linux / WSL (Ubuntu)

Recomendado para ambientes de produção ou desenvolvimento avançado.

### 1. Preparação Automática

No terminal do Linux (Bash), navegue até a pasta do projeto e execute:

```bash
cd /mnt/d/HACKTHON1  # Ajuste o caminho conforme necessário

# Dar permissão e rodar o script de setup automático
chmod +x setup_linux.sh
./setup_linux.sh
```

*Este script instala o Python venv, cria o ambiente e instala todas as dependências automaticamente.*

### 2. Rodar a API

O script acima cria um atalho. Apenas execute:

```bash
./run_api.sh
```

> Mantenha este terminal aberto.

### 3. Rodar o Frontend

Em outro terminal Linux:

```bash
cd frontend
npm install
npm run dev
```

---

## 🚑 Solução de Problemas Comuns

### ❌ Erro: "Port 8000 is already in use"

Isso significa que você já tentou rodar a API antes e ela ainda está presa em segundo plano.
**Solução (Windows):**

```powershell
# Descobrir o PID (número do processo)
netstat -ano | findstr :8000
# Matar o processo (substitua PID pelo número que apareceu)
taskkill /F /PID <NUMERO_DO_PID>
```

### ❌ Erro: "python não é reconhecido"

O Python não está no PATH do Windows ou não foi instalado.
**Solução:** Tente usar `python3` ou reinstale o Python marcando "Add to PATH".

### ❌ Erro: "npm não é reconhecido"

O Node.js não foi instalado corretamente.
**Solução:** Reinicie o terminal ou o computador após instalar o Node.js.

### ❌ Erro: "Scikit-learn não encontrado" (No Backend)

O sistema entrará automaticamente em **Modo Mock (Fallback)**.
**Isso é normal** se você não conseguir instalar pacotes compilados C++ no seu ambiente. O projeto continuará funcionando perfeitamente com simulação.

---

**Equipe Hackathon One 8 Alura**
