# Título do PR

🚀 Release Candidate: v1.0.0-MVP - ChurnInsight Platform

# Descrição

Este Pull Request consolida todo o trabalho de desenvolvimento do MVP para a Plataforma de Previsão de Churn. Ele mergeia a branch de desenvolvimento (`develop`) na branch principal (`main`) para o lançamento oficial da versão 1.0.0.

## 📦 O que foi entregue?

- **Backend (API)**: Pipeline completo de Machine Learning (Treino + Inferência) com FastAPI e suporte a Fallback (Mock Model).
- **Frontend (UI)**: Interface React moderna para simulação de churn em tempo real.
- **Documentação**: Manuais de Instalação, Guia de Simulação (Windows/WSL) e Readme Otimizado.
- **QA**: Testes automatizados (`test_model.py`, `test_api_request.py`) e validação E2E manual.

## 🧪 Validação Realizada

- [x] Build do Frontend (Vite) com sucesso.
- [x] API respondendo em `localhost:8000/predict`.
- [x] Teste de Carga Simples (Simulação de múltiplos cenários).
- [x] Linting e organização de código (Gitignore, Remoção de node_modules).

## 📸 Screenshots (Evidências)

O relatório de validação técnica pode ser encontrado em: [`RELATORIO_VALIDACAO.md`](./RELATORIO_VALIDACAO.md).

## 🚀 Próximos Passos (Post-Merge)

Após este merge, o foco do time será na **Fase 2**:

1. Containerização (Docker Compose).
2. Integração com Banco de Dados PostgreSQL.

---
*Este PR fecha a issue #1 (Lançamento MVP).*
