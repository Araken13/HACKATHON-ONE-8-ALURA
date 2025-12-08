# 📋 Checklist Fase 2 - Evolução do ChurnInsight

Com o MVP (API + Modelo) finalizado, iniciaremos a Fase 2 focada em **robustez, dados e visualização**.

## 1. Containerização (DevOps) 🐳

- [ ] **Criar Dockerfile**: Empacotar a aplicação Python (API + dependências) em uma imagem Docker.
- [ ] **Criar docker-compose.yml**: Orquestrar o serviço da API para rodar com um comando.

## 2. Persistência de Dados (Banco de Dados) 🗄️

- [ ] **Configurar SQLite/PostgreSQL**: Adicionar uma camada de banco de dados.
- [ ] **Modelar Tabela de Histórico**: Criar tabela para salvar cada requisição recebida (`inputs`) e a previsão gerada (`output`, `data_hora`).
- [ ] **Atualizar API**: Modificar o endpoint `/predict` para salvar os dados no banco antes de retornar.

## 3. Novos Endpoints (Backend) 📡

- [ ] **GET /stats**: Endpoint para retornar estatísticas gerais (Ex: "Total de previsões: 150", "Taxa de Churn prevista: 25%").
- [ ] **POST /predict/batch**: Endpoint para receber um arquivo CSV ou lista JSON e processar múltiplos clientes de uma vez.

## 4. Frontend / Dashboard 📊

- [ ] **Criar App Streamlit**: Construir uma interface gráfica simples em Python.
  - Upload de arquivo CSV para previsão em massa.
  - Formulário para testar um cliente manualmente.
  - Gráficos das estatísticas (usando o endpoint `/stats` ou lendo do banco).

## 5. Qualidade e Testes 🧪

- [ ] **Testes Unitários**: Melhorar `test_model.py` usando `pytest`.
- [ ] **Testes de Integração**: Automatizar o teste da API garantindo que o banco está sendo gravado.

---
**Recomendação de Prioridade:**
Sugiro começar pela **Persistência (2)** e **GET /stats (3)**, pois agregam valor imediato ao negócio (histórico). Depois **Docker (1)** e por fim **Dashboard (4)**.
