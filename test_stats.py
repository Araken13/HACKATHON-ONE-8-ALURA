import requests
import time

url_base = "http://127.0.0.1:8000"

def get_stats():
    try:
        resp = requests.get(f"{url_base}/stats")
        if resp.status_code == 200:
            print(f"📊 STATS: {resp.json()}")
        else:
            print(f"Erro ao pegar stats: {resp.status_code}")
    except Exception as e:
        print(f"API fora do ar? {e}")

def create_prediction():
    payload = {
        "idade": 25,
        "tempo_assinatura_meses": 1,
        "plano_assinatura": "basico",
        "valor_mensal": 19.90,
        "visualizacoes_mes": 5,
        "tempo_medio_sessao_min": 10,
        "contatos_suporte": 10,
        "avaliacao_conteudo": 1.0, 
        "metodo_pagamento": "boleto",
        "dispositivo_principal": "mobile"
    }
    try:
        resp = requests.post(f"{url_base}/predict", json=payload)
        if resp.status_code == 200:
            print(f"✅ Previsão Criada! Risco Alto? {resp.json()['risco_alto']}")
        else:
            print(f"Erro na previsão: {resp.status_code}")
    except:
        pass

print("--- ANTES ---")
get_stats()

print("\n--- GERANDO DADO NOVO... ---")
create_prediction()
time.sleep(1) # Esperar persistência (SQLite é rápido, mas safe)

print("\n--- DEPOIS ---")
get_stats()
