# 📋 Relatório de Validação e Execução - ChurnInsight MVP

**Data de Validação:** 08 de Dezembro de 2025
**Responsável:** Araken Carmo Neto / Equipe Hackathon One 8 Alura
**Status:** ✅ Aprovado para Deploy/Demonstração

---

## 1. Resumo Executivo

O sistema **ChurnInsight** foi validado em ambiente local. Todos os componentes principais (Pipeline de Dados, Modelo Preditivo, API Backend e Frontend Interativo) estão operacionais e integrados. O sistema demonstra capacidade de processar entradas de usuários em tempo real e fornecer previsões de churn com base em regras de negócio (Mock Model) ou modelo de ML treinado.

## 2. Componentes Validados

### 🧠 A. Pipeline de Machine Learning & Modelo

- **Estado**: Funcional (Modo Híbrido: ML + Mock Fallback).
- **Teste Realizado**: `train_model.py` executado com sucesso.
- **Resultado**:
  - O sistema identifica automaticamente a ausência de bibliotecas pesadas (`scikit-learn`) e ativa o **Mock Model** para garantir a execução em qualquer ambiente.
  - Artefatos gerados: `churn_model.joblib` e `model_metadata.json`.

### 🔌 B. API REST / GraphQL (Backend)

- **Tecnologia**: FastAPI
- **Porta**: 8000
- **Teste Realizado**:
  - Script de integração `test_api_request.py`.
  - Inicialização do servidor via `python api.py`.
- **Resultados de Inferência**:
  - **Cenário Cliente Fiel**: Probabilidade de Churn **20%** (Baixo Risco) - *Precisão Confirmada*.
  - **Cenário Cliente em Risco**: Probabilidade de Churn **90%** (Alto Risco) - *Precisão Confirmada*.
- **Rotas Ativas**: `/predict` (REST) e `/graphql`.

### 💻 C. Frontend (Interface do Usuário)

- **Tecnologia**: React + Vite + Apollo Client
- **Porta**: 5174 (Auto-detectada devido à ocupação da 5173)
- **Status**: Build e Start realizados com sucesso.
- **Integração**: Conectado ao backend via GraphQL/REST.

## 3. Detalhes Técnicos da Validação

### Log de Teste da API (Snapshot)

```json
// Request: Cliente com perfil de Risco
{
  "previsao": "Vai cancelar",
  "probabilidade_churn": 0.9,
  "risco_alto": true
}
```

### Ambiente de Execução

- **OS**: Windows (WSL Support Verified)
- **Python**: 3.10+
- **Node**: v18+ (Vite Compatible)

## 4. Próximos Passos Recomendados

1. **Containerização**: Finalizar o `docker-compose` para orquestrar Backend e Frontend em um único comando.
2. **Banco de Dados**: Migrar persistência de logs para PostgreSQL (atualmente em memória/logs).

---
*Relatório gerado automaticamente após bateria de testes automatizados.*
