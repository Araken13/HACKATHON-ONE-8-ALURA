# Especificação Técnica do Projeto - Plataforma de Análise de Churn

## 1. Visão Geral

Este documento descreve a arquitetura técnica, as escolhas tecnológicas e a metodologia de desenvolvimento aplicada na construção da plataforma "ChurnInsight". O objetivo do sistema é prever a rotatividade (churn) de clientes de serviços de streaming, processar dados em lote e oferecer visualizações analíticas em tempo real.

---

## 2. Metodologia de Desenvolvimento

O projeto foi desenvolvido seguindo uma abordagem **Iterativa e Incremental**, focada em entrega contínua de valor e validação técnica passo a passo. O ambiente de desenvolvimento primário foi o **WSL (Windows Subsystem for Linux)**, garantindo compatibilidade com ambientes de produção Linux desde o início.

### Fases do Desenvolvimento

1. **Fundação e Modelagem (Data Science)**:
    * Análise exploratória de dados e treinamento de modelos de Machine Learning (Scikit-Learn).
    * Exportação do modelo treinado (`.joblib`) para inferência.
2. **Desenvolvimento da API (Backend)**:
    * Criação da API com **FastAPI** para expor o modelo.
    * Implementação de rotas REST para inferência unitária e em lote (`/predict`, `/predict/batch`).
    * Adição de suporte a **GraphQL** para consultas flexíveis.
3. **Persistência e Dados**:
    * Modelagem do banco de dados relacional.
    * Migração de SQLite (MVP) para **PostgreSQL** (Produção).
4. **Containerização e Orquestração**:
    * Criação de `Dockerfiles` otimizados para cada serviço.
    * Orquestração completa via **Docker Compose** para subir API, Banco, Frontend e Grafana simultaneamente.
5. **Analytics e Frontend**:
    * Integração do **Grafana** conectado diretamente ao PostgreSQL para dashboards em tempo real.
    * Desenvolvimento de interface interativa com **React** e **Vite**.

---

## 3. Arquitetura do Sistema

A solução segue uma arquitetura baseada em **Microsserviços** (gerenciados via Docker Compose), onde cada componente tem uma responsabilidade única e desacoplada.

### Diagrama Lógico

```
[Frontend (React)] <--> [API Gateway (FastAPI)] <--> [ML Model (Scikit-Learn)]
                                   |
                                   v
                            [PostgreSQL (Persistência)]
                                   ^
                                   |
                            [Grafana (Analytics)]
```

### Componentes

1. **Frontend (UI)**: Interface SPA (Single Page Application) para interação do usuário.
2. **Backend (API)**: Cérebro do sistema. Gerencia requisições, valida dados (Pydantic), executa o modelo de IA e persiste históricos.
3. **Database (OLTP/OLAP)**: Armazena histórico de previsões e metadados de clientes. Servindo tanto para transações da API quanto para consultas analíticas do Grafana.
4. **Analytics**: Painéis de visualização de métricas de negócio (Taxa de Churn, Risco por Perfil).

---

## 4. Stack Tecnológico e Justificativas

Escolhemos tecnologias modernas, performáticas e amplamente adotadas pelo mercado para garantir robustez e manutenibilidade.

### **Backend: FastAPI (Python)**

* **Por que escolhemos?**
  * **Performance**: É um dos frameworks Python mais rápidos, graças ao uso de `Starlette` e `Pydantic`.
  * **Produtividade**: Gera documentação automática (Swagger/OpenAPI), essencial para testar endpoints durante o dev.
  * **Async**: Suporte nativo a concorrência assíncrona, crucial para não bloquear o servidor durante processamento de IA ou chamadas de banco.
  * **Integração com IA**: Python é a linguagem nativa de Data Science, facilitando o carregamento direto do modelo `.joblib` sem "gambiarras" de integração.

### **Banco de Dados: PostgreSQL**

* **Por que escolhemos?**
  * **Robustez**: Banco relacional mais avançado do mercado open-source.
  * **JSONB**: Suporte nativo a dados semi-estruturados, permitindo salvar o input variável do cliente (`cliente_input`) sem rigidez excessiva de schema.
  * **Confiabilidade**: Garante ACID, essencial para dados de negócio.
  * **Compatibilidade**: Funciona perfeitamente com Grafana e SQLAlchemy.

### **Frontend: React + Vite**

* **Por que escolhemos?**
  * **Vite**: Build tool extremamente rápida (Subistituto moderno do Webpack). Permite HMR (Hot Module Replacement) instantâneo.
  * **React**: Biblioteca de UI mais popular, com vasto ecossistema de componentes. Facilita a criação de interfaces reativas e dinâmicas.

### **Analytics: Grafana**

* **Por que escolhemos?**
  * **Especialização**: Ao invés de "reinventar a roda" construindo gráficos complexos no React, usamos o Grafana que é especializado em observabilidade.
  * **Conexão Direta**: Conecta nativamente ao Postgres, permitindo criar dashboards SQL em minutos.
  * **Alocação de Esforço**: Permitiu focar o desenvolvimento de código na IA e API, enquanto a visualização ficou a cargo de uma ferramenta No-Code robusta.

### **Infraestrutura: Docker & Docker Compose**

* **Por que escolhemos?**
  * **Imutabilidade**: Garantia de que o código roda igual no Windows do desenvolvedor e no servidor Linux de produção.
  * **Setup Rápido**: Com um comando (`docker compose up`), todo o ecossistema (4 serviços) é levantado e configurado automaticamente.

---

## 5. Qualidade e Testes (QA)

A garantia de qualidade foi assegurada através de:

* **Testes Unitários**: Validação de funções isoladas (ex: pré-processamento de dados).
* **Testes de Integração**: Testes da API (`test_api_request.py`) verificando o fluxo completo de Request -> Model -> Response.
* **Testes de Carga**: Validação de processamento em lote com arquivos CSV reais.

---

## 6. Conclusão

A arquitetura definida é **escalável** (containers podem ser replicados em Kubernetes futuramente), **moderna** (uso de FastAPI e React) e **orientada a dados** (Postgres + Grafana no centro da decisão). Ela atende aos requisitos funcionais de prever churn e aos não-funcionais de manutenibilidade e observabilidade.
