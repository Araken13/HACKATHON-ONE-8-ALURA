# 🕵️ Relatório de Auditoria Técnica - ChurnInsight v1.0

Realizams uma análise estática profunda nos artefatos do projeto. Abaixo estão os pontos de atenção identificados que precisam ser corrigidos antes da Containerização (Fase 2).

## 1. Backend API (`api.py`) - 🔴 Crítico

### Problema: Binding de Host Local

Na linha 206:

```python
uvicorn.run(app, host="127.0.0.1", port=8000)
```

O endereço `127.0.0.1` faz a API escutar apenas conexões de dentro da própria máquina (localhost).

### Impacto

Quando rodar no **Docker**, o container terá seu próprio "localhost". Se a API ouvir apenas nele, o Docker (externo) não conseguirá acessar a porta 8000. **Ninguém conseguirá acessar a API.**

### Solução Recomendada

Alterar para `0.0.0.0` (Listen All Interfaces) ou usar variável de ambiente:

```python
host = os.getenv("API_HOST", "127.0.0.1")
uvicorn.run(app, host=host, port=8000)
```

---

## 2. Dockerfile - 🟡 Médio

### Problema A: Dependências Hardcoded

O arquivo instala libs manualmente (`RUN pip install pandas ...`) em vez de usar `requirements.txt`.

- **Risco**: Se atualizarmos uma versão no `requirements.txt`, o Docker continuará usando a versão velha hardcoded, causando "bugs fantasmas".

### Problema B: Camada de Cache

O comando `COPY . .` vem logo após a instalação. Isso é aceitável, mas em projetos maiores, copiamos o `requirements.txt` primeiro para aproveitar o cache do Docker.

---

## 3. Banco de Dados (`init.sql`) - 🟢 Bom

O script de inicialização está excelente.

- ✅ Usa `IF NOT EXISTS` para evitar erros.
- ✅ Cria índices de performance (`idx_risco_alto`).
- ✅ Define RLS (Row Level Security) e Triggers, demonstrando maturidade.

---

## 4. Frontend - 🟡 Observação

O teste E2E revelou que o formulário React não envia todos os campos que o Modelo Python espera (ex: `tempo_assinatura_meses` e `plano_assinatura` faltam no UI).

- **Impacto**: O modelo usa valores default (seguros), o que subestima o risco de churn em simulações manuais.
- **Ação**: Adicionar os campos faltantes no componente React `Home.tsx` (ou equivalente).

---

## Conclusão

O código é sólido, mas a **configuração de rede do Python (`api.py`) quebrará a implantação Docker** se não for ajustada.
