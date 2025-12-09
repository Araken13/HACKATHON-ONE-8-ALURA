# 📘 Manual do Usuário - ChurnInsight

Bem-vindo à plataforma de Inteligência Artificial para Retenção de Clientes. Este documento guia você através das principais funcionalidades do sistema.

## 1. Visão Geral (Dashboard)

Ao acessar o sistema (`http://localhost:5173`), você verá os indicadores principais (KPIs) no topo:

- **Total Analisado**: Quantidade de clientes processados até agora.
- **Risco Previsto**: Clientes identificados pela IA com alta probabilidade de cancelamento.
- **Taxa de Churn**: Porcentagem da base em risco.

## 2. Simulador de Cenários em Tempo Real ⚡

Localizado à esquerda na tela principal.

- **Como usar:** Preencha os dados de um cliente hipotético (Idade, Mensalidade, Suporte, etc).
- **Ação:** Clique em **"Simular Impacto"**.
- **Resultado:** A IA dirá instantaneamente se esse perfil tende a cancelar ("Vai cancelar") ou ficar ("Vai continuar"), junto com a probabilidade (ex: 85%).
- **Dica:** Tente aumentar o valor da mensalidade para ver em que ponto o cliente desiste!

## 3. Processamento em Lote (Batch) 📂

Para analisar sua base de clientes real (milhares de linhas).

1. Prepare um arquivo `.csv` com os dados dos clientes.
2. Na caixa "Processamento em Lote", clique e selecione seu arquivo.
3. O sistema fará o upload, processará cada linha na IA e **baixará automaticamente** um novo arquivo.
4. Abra o novo arquivo: ele terá uma coluna extra `previsao_churn` com o veredito.

## 4. Sandbox de Negócios (Business Intelligence) 🧪

Uma ferramenta poderosa para prever o futuro.

- **Gerar Massa de Dados:**
    1. Role até o final da página.
    2. Digite a quantidade de clientes virtuais (ex: 1000).
    3. Clique em **"Baixar Dataset Sintético"**.
- **Analisar o Futuro:**
    1. Pegue o arquivo gerado pelo Sandbox.
    2. Suba na ferramenta de **Processamento em Lote**.
    3. **Insight:** Descubra quantos desses "novos clientes" teriam alta probabilidade de churn antes mesmo de eles entrarem!

---
**Suporte Técnico**
Para reiniciar o sistema, execute `start_platform.bat` ou contate a equipe de Data Science.
