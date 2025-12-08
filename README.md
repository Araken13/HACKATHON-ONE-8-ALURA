# 🔮 ChurnInsight - Previsão de Churn (MVP)

Projeto desenvolvido durante o Hackathon One 8 Alura. O objetivo é fornecer uma solução completa de Data Science e Engenharia de Backend para prever a probabilidade de cancelamento (Churn) de clientes de um serviço de streaming.

## 🚀 Funcionalidades

- **Pipeline de Dados**: Limpeza, tratamento de valores nulos e encoding de variáveis categóricas.
- **Modelo Preditivo**: Classificação binária ("Vai cancelar" vs "Vai continuar") utilizando Random Forest (com fallback robusto para ambientes restritos).
- **API REST**: Microserviço em Python (FastAPI) de alta performance para servir o modelo.
- **Validação de Contrato**: Entrada de dados tipada e validada via Pydantic.
- **Metadados Inteligentes**: Sincronização automática de encodings entre treino e inferência para evitar erros de consistência.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.10+
- **Data Science**: Pandas, Scikit-learn, Numpy, Joblib
- **API**: FastAPI, Uvicorn, Pydantic
- **Ferramentas**: Git, WSL (Windows Subsystem for Linux)

## 📂 Estrutura do Projeto

```bash
📦 HACKATHON-ONE-8-ALURA
├── 📄 dataset_churn_...csv    # Base de dados original
├── 📄 train_model.py          # Script de pipeline (Limpeza + Treinamento)
├── 📄 api.py                  # Servidor da API (FastAPI)
├── 📄 test_model.py           # Teste unitário do modelo
├── 📄 test_api_request.py     # Script de teste de integração com a API
├── 📄 churn_model.joblib      # Artefato do modelo treinado (binário)
├── 📄 model_metadata.json     # Metadados para garantir consistência da API
└── 📄 README.md               # Documentação
```

## ⚡ Como Rodar o Projeto

### 1. Preparar o Ambiente

Recomendamos o uso de um ambiente virtual (venv).

```bash
# Instalar dependências
pip install pandas scikit-learn joblib numpy fastapi uvicorn requests
```

### 2. Treinar o Modelo

Execute o pipeline para processar os dados e gerar o artefato do modelo (`.joblib`).

```bash
python train_model.py
```

*Saída esperada: "Pipeline finalizado com sucesso. Modelo e metadados salvos."*

### 3. Iniciar a API

Suba o servidor localmente na porta 8000.

```bash
python api.py
```

*Acesse a documentação interativa em: <http://127.0.0.1:8000/docs>*

### 4. Testar Previsão

Em outro terminal, execute o script de teste ou faça uma requisição manual.

```bash
python test_api_request.py
```

#### Exemplo de Payload (Request)

```json
POST /predict
{
  "idade": 40,
  "tempo_assinatura_meses": 2,
  "plano_assinatura": "basico",
  "valor_mensal": 19.90,
  "visualizacoes_mes": 10,
  "tempo_medio_sessao_min": 15,
  "contatos_suporte": 5,
  "avaliacao_conteudo": 1.5,
  "metodo_pagamento": "boleto",
  "dispositivo_principal": "tv"
}
```

#### Exemplo de Resposta

```json
{
  "previsao": "Vai cancelar",
  "probabilidade_churn": 0.9,
  "risco_alto": true
}
```

## 📈 Próximos Passos (Roadmap)

Para evoluir este MVP para um produto final robusto, planejamos as seguintes etapas:

1. **🐳 Containerização**: Criar `Dockerfile` e `docker-compose.yml` para facilitar o deploy e garantir reproducibilidade do ambiente.
2. **🗄️ Persistência de Dados**: Integrar um banco de dados (PostgreSQL ou SQLite) para salvar o histórico de todas as previsões realizadas pela API.
3. **📊 Dashboard de Monitoramento**: Criar uma interface visual (Streamlit ou React) para acompanhar em tempo real os clientes de alto risco identificados.
4. **🔄 Pipeline de CI/CD**: Automatizar o retreino do modelo (MLOps) sempre que novos dados do `dataset` forem adicionados ao repositório.
5. **🔐 Autenticação**: Proteger a API com chave de acesso (API Key) ou OAuth2.

---
*Desenvolvido com 💻 e ☕ por [Seu Nome/Time]*
