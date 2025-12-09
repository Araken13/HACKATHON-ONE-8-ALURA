import requests
import time

print("Aguardando API iniciar...")
time.sleep(3) # Dar um tempinho pro servidor subir

url = "http://127.0.0.1:8000/predict"

# 1. Cliente Feliz (Fiel)
payload_fiel = {
    "idade": 30,
    "tempo_assinatura_meses": 24,
    "plano_assinatura": "premium",
    "valor_mensal": 39.90,
    "visualizacoes_mes": 50,
    "tempo_medio_sessao_min": 60,
    "contatos_suporte": 0,
    "avaliacao_conteudo": 5.0,
    "metodo_pagamento": "credito",
    "dispositivo_principal": "mobile"
}

# 2. Cliente Irritado (Churn)
payload_churn = {
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

try:
    print(f"\nEnviando requisição FIEL para {url}...")
    resp = requests.post(url, json=payload_fiel)
    print(f"Status: {resp.status_code}")
    print(f"Resposta: {resp.json()}")

    print(f"\nEnviando requisição CHURN para {url}...")
    resp = requests.post(url, json=payload_churn)
    print(f"Status: {resp.status_code}")
    print(f"Resposta: {resp.json()}")

except Exception as e:
    print(f"Deu ruim na conexão: {e}")
    print("A API tá rodando mesmo? Verifique o terminal anterior.")
