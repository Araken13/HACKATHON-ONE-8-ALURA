# 🔮 ChurnInsight: AI-Powered Customer Retention Platform

[![Manual de Instalação](https://img.shields.io/badge/Instalação-PASSO%20A%20PASSO-success?style=for-the-badge)](./docs/MANUAL_INSTALACAO.md)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
![GraphQL](https://img.shields.io/badge/-GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)

> **Preveja o futuro, retenha seus clientes.**
> O ChurnInsight é uma solução completa de **Analytics & Machine Learning** projetada para identificar clientes em risco de cancelamento (Churn) em serviços de streaming, permitindo ações proativas de retenção.

---

## 📋 Sobre o Projeto

O **ChurnInsight** não é apenas um modelo preditivo; é um ecossistema completo de engenharia de dados e software. Ele combina um backend robusto em **Python/FastAPI** com um frontend moderno em **React**, utilizando **Machine Learning (Random Forest)** para analisar padrões de comportamento de usuários em tempo real.

Desenvolvido durante o **Hackathon One 8 Alura**, este projeto demonstra a aplicação prática de Data Science em problemas reais de negócio.

### 🌟 Diferenciais

- **Pipelines Robustos**: Tratamento automático de dados sujos, nulos e encoding de variáveis.
- **Hybrid AI Core**: Funciona com modelos treinados (Scikit-learn) ou Fallback Lógico Inteligente para ambientes leves.
- **Arquitetura Moderna**: API REST + GraphQL servindo um Frontend reativo.
- **Developer Experience**: Scripts de automação para testes, treino e setup.

---

## 🚀 Stack Tecnológico

### Backend & Data Science

- **Linguagem**: Python 3.10+
- **API Framework**: FastAPI (Alta performance, Async I/O)
- **ML & Dados**: Pandas, Scikit-learn, Joblib, Numpy
- **Qualidade**: Pydantic para validação rigorosa de dados

### Frontend

- **Framework**: React 18
- **Build Tool**: Vite (Ultra-rápido)
- **Data Fetching**: Apollo Client (GraphQL Integation)
- **Linguagem**: TypeScript / JavaScript

---

## 📂 Estrutura do Repositório

```bash
📦 CHURN-INSIGHT
├── 📂 analytics          # Dashboards e Análises Exploratórias
├── 📂 docs               # Documentação Completa (Guias, Manuais)
├── 📂 frontend           # Aplicação Web (React/Vite)
├── 📂 scripts            # Scripts Utilitários (Setup, Automação)
├── 📂 tests              # Testes Automatizados
├── 📄 api.py             # Gateway da API (FastAPI + GraphQL)
├── 📄 train_model.py     # Pipeline de Treinamento de ML
├── 📄 churn_model.joblib # Artefato do Modelo Serializado
└── 📄 requirements.txt   # Dependências do Backend
```

---

## ⚡ Guia de Início Rápido (Quickstart)

### 1. Backend Setup

```bash
# Instale as dependências
pip install -r requirements.txt

# Treine o modelo (Gera o arquivo joblib)
python train_model.py

# Inicie a API (Disponível em http://localhost:8000)
python api.py
```

### 2. Frontend Setup

```bash
cd frontend

# Instale os pacotes npm
npm install

# Inicie a interface (Disponível em http://localhost:5173 ou 5174)
npm run dev
```

### 💡 Simulação Avançada (Windows vs WSL)

Quer testar como um profissional usando Windows ou Linux (WSL)?
👉 **[Leia o Guia de Simulação Completo](./docs/GUIA_SIMULACAO_WIN_WSL.md)**

---

## 🧠 Como Funciona a Inteligência Artificial

O modelo analisa variáveis comportamentais chave para calcular o `churn_probability`:

| Variável | Impacto na Previsão |
|----------|---------------------|
| `tempo_assinatura_meses` | Clientes recentes (< 3 meses) têm maior risco. |
| `avaliacao_conteudo` | Notas baixas são fortes indicativos de insatisfação. |
| `visualizacoes_mes` | Baixo engajamento correlaciona com cancelamento. |
| `contatos_suporte` | Alto volume de contatos indica problemas técnicos/fustração. |

---

## 🧪 Testes e Validação

O projeto inclui uma suíte de testes automatizados para garantir a estabilidade:

- **Teste de Modelo**: `python tests/test_model.py` (Valida a acurácia das previsões).
- **Teste de Integração API**: `python tests/test_api_request.py` (Simula requisições reais HTTP).

Para ver os resultados da última execução, consulte o arquivo [RELATORIO_VALIDACAO.md](./docs/RELATORIO_VALIDACAO.md).

---

## 🗺️ Roadmap de Evolução

- [x] **MVP**: API Preditiva + Frontend Básico
- [x] **Integração GraphQL**: Consultas otimizadas
- [x] **Docker Compose**: Orquestração completa do ambiente
- [x] **Banco de Dados Real**: Migração para PostgreSQL
- [x] **Dashboard Analytics**: Gráficos de tendências de churn

## 📚 Documentação Técnica

Para detalhes profundos sobre a arquitetura, decisões técnicas e infraestrutura, leia a [Especificação Técnica Completa](./ESPECIFICACAO_TECNICA.md).

---

<div align="center">
  <p>Desenvolvido com 💙 por <strong>Araken Carmo Neto</strong> no Hackathon One Alura</p>
  <p>
    <a href="https://linkedin.com/in/araken">LinkedIn</a> •
    <a href="https://github.com/Araken13">GitHub</a>
  </p>
</div>
