# 🧪 Guia de Simulação: Windows vs WSL (Linux)

Este guia orienta como operar e validar o projeto **ChurnInsight** tanto no ambiente nativo Windows quanto no Subsistema Linux (WSL), simulando cenários reais de desenvolvimento e produção.

---

## 🖥️ 1. Cenário Windows (Ambiente Atual)

Atualmente, seus terminais Windows estão rodando os serviços. Este é o cenário típico de **Desenvolvimento Local Rápido**.

### 🚦 Status Atual

- **Backend (API)**: Rodando em `Powershell` na porta **8000**.
- **Frontend**: Rodando em `Powershell` na porta **5174**.

### 🎮 Como Simular o Uso

1. **Acesse o Frontend**:
   - Abra o navegador em: [http://localhost:5174](http://localhost:5174)
   - Preencha o formulário com dados de teste.
   - Clique em "Prever".
   - **O que acontece**: O React (JS) no navegador manda um JSON para o Python no Windows, que processa e devolve a resposta.

2. **Teste via Terminal (cURL/PowerShell)**:
   Abra um novo terminal Windows e rode:

   ```powershell
   Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -ContentType "application/json" -Body '{"idade": 30, "tempo_assinatura_meses": 2, "plano_assinatura": "basico", "visualizacoes_mes": 10, "tempo_medio_sessao_min": 15, "contatos_suporte": 5, "avaliacao_conteudo": 1.5, "valor_mensal": 19.9, "metodo_pagamento": "boleto", "dispositivo_principal": "tv"}' -Encoding UTF8
   ```

---

## 🐧 2. Cenário WSL (Simulação de Servidor Linux)

Este cenário simula como o código rodaria em produção (Servidor Ubuntu/Debian) ou em um ambiente de desenvolvimento isolado.

### 📝 Pré-requisitos

- WSL instalado e rodando (Ubuntu).
- A pasta do projeto no WSL é acessível via `/mnt/d/HACKTHON1`.

### 👣 Passo a Passo para Migrar para WSL

#### Passo 1: Acesse o WSL

Abra seu terminal WSL (Ubuntu) e navegue até a pasta:

```bash
cd /mnt/d/HACKTHON1
```

#### Passo 2: Configure o Ambiente Linux

Você já possui um script automatizado (`setup_linux.sh`) para isso. Execute:

```bash
# Dar permissão de execução
chmod +x setup_linux.sh

# Rodar o setup (instala venv, pip, libs)
./setup_linux.sh
```

#### Passo 3: Rode a API no Linux

O setup cria um script de atalho `run_api.sh`. Use-o:

```bash
# Isso vai subir a API na porta 8000 do LINUX (mas acessível pelo Windows como localhost:8000)
./run_api.sh
```

> **⚠️ Importante**: Se a API do Windows ainda estiver rodando, você terá um **Conflito de Porta**.
> Para testar no WSL, pare o terminal do Python no Windows (Ctrl+C) primeiro!

### 🧪 Diferenças Chave na Simulação

| Característica | Windows (Powershell) | WSL (Ubuntu) |
| :--- | :--- | :--- |
| **Sistema de Arquivos** | `D:\HACKTHON1` | `/mnt/d/HACKTHON1` |
| **Execução Python** | `python api.py` | `./run_api.sh` (via gunicorn/uvicorn direto) |
| **Performance** | Nativa (GUI rápida) | Mais próxima de Produção (Docker friendly) |
| **Scripts** | `.bat` ou manual | `.sh` (Shell Script) |

---

## 🔄 3. Ciclo de Teste Híbrido

Para garantir robustez, siga este fluxo:

1. **Codifique no Windows**: Use o VS Code no Windows para editar arquivos.
2. **Valide no WSL**:
   - Abra o terminal integrado do VS Code.
   - Mude o perfil do terminal para "WSL: Ubuntu".
   - Rode os testes unitários lá:

     ```bash
     ./venv/bin/python test_model.py
     ```

Isso garante que seu código funcione em ambos os sistemas operacionais, prevenindo o clássico problema *"na minha máquina funciona"*.
