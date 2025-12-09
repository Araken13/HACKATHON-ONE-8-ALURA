# 📄 Relatório Técnico: Batch Prediction (Previsão em Lote)

## 📌 1. Visão Geral

A funcionalidade de **Batch Prediction** permite que o sistema ChurnInsight processe grandes volumes de dados de clientes de uma única vez, substituindo a necessidade de consultas manuais individuais. Isso é essencial para operações de escala, como campanhas de marketing ou auditorias mensais.

---

## ⚙️ 2. Como Funciona (Fluxo Técnico)

1. **Entrada (Input)**:
    * O usuário (ou sistema externo) envia um arquivo **CSV** contendo milhares de linhas.
    * Cada linha representa um cliente com seus atributos (idade, plano, uso, etc.).

2. **Processamento na API**:
    * O endpoint `POST /predict/batch` recebe o arquivo via *stream*.
    * Os dados são carregados em memória usando a biblioteca **Pandas** (DataFrame).
    * A API aplica o pipeline de pré-processamento (limpeza + encoding) em todas as linhas simultaneamente (vetorização), o que é milhares de vezes mais rápido do que loops tradicionais.
    * O Modelo de IA (Random Forest) recebe a matriz de dados e gera dois vetores:
        * `previsao`: 0 ou 1 (Ficar ou Sair).
        * `probabilidade`: 0.0 a 1.0 (Risco).

3. **Saída (Output)**:
    * A API anexa essas duas novas colunas ao CSV original.
    * O arquivo resultante é devolvido via download automático para o solicitante.

---

## 🧪 3. Cenário de Uso (Exemplo Prático)

### A. O Problema

O time de Marketing quer disparar um e-mail com cupom de desconto apenas para clientes com **Alto Risco** de cancelamento antes que o mês vire. Eles têm uma base de 50.000 clientes ativos.

### B. A Execução

1. O analista exporta a base do CRM para `clientes_dezembro.csv`.
2. Ele envia esse arquivo para nosso sistema:

    ```bash
    POST http://api-churn/predict/batch
    File: clientes_dezembro.csv
    ```

3. Em alguns segundos, ele recebe de volta `previsoes_churn.csv`.

### C. O Resultado

O arquivo de retorno contém:

| Cliente ID | Plano | ... | **Previsão** | **Probabilidade** |
| :--- | :--- | :--- | :--- | :--- |
| 1001 | Basic | ... | Vai continuar | 0.12 |
| 1002 | Premium | ... | **Vai cancelar** | **0.89** |

O analista filtra quem tem `Probabilidade > 0.8` e manda a campanha de retenção apenas para esses, otimizando o orçamento.

---

## 🚀 4. Performance e Escalabilidade

* **Tempo Estimado**: Para 3.000 registros, o processamento leva menos de **0.5 segundos** (graças ao Pandas/Numpy).
* **Limitações Atuais**: O arquivo deve caber na memória RAM do servidor. Para arquivos gigantes (Gigabytes), seria necessário evoluir para processamento em *chunks* (pedaços) ou usar filas (Celery/Kafka), mas para o escopo atual (até ~500k linhas), nossa solução atende perfeitamente.
