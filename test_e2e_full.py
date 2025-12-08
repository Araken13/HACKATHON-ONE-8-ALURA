import requests
import io
import pandas as pd
import json

BASE_URL = "http://127.0.0.1:8000"

def log(msg, status="INFO"):
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "FAIL": "❌", "WARN": "⚠️"}
    print(f"{icons.get(status, '')} [{status}] {msg}")

def test_health():
    log("Testando Healthcheck...")
    try:
        r = requests.get(f"{BASE_URL}/")
        if r.status_code == 200:
            log("API Online", "SUCCESS")
        else:
            log(f"API Offline ou Erro: {r.status_code}", "FAIL")
            exit(1)
    except Exception as e:
        log(f"Falha de conexão: {e}", "FAIL")
        exit(1)

def test_graphql_stats():
    log("Testando GraphQL Stats...")
    query = """
    query {
      stats {
        totalAnalisados
        taxaRiscoPercentual
      }
    }
    """
    r = requests.post(f"{BASE_URL}/graphql", json={'query': query})
    if r.status_code == 200 and "data" in r.json():
        data = r.json()['data']['stats']
        log(f"Stats Recebidos: Total={data['totalAnalisados']}, Taxa={data['taxaRiscoPercentual']}%", "SUCCESS")
    else:
        log(f"Erro no GraphQL: {r.text}", "FAIL")

def test_graphql_simulation():
    log("Testando Simulação de Cenário (Cliente Ruim)...")
    # Cliente propenso a cancelar (mensalidade alta, nota baixa)
    query = """
    query {
      analiseChurn(cliente: {
        idade: 25,
        tempoAssinaturaMeses: 1,
        planoAssinatura: "Premium",
        valorMensal: 89.90,
        visualizacoesMes: 5,
        tempoMedioSessaoMin: 10,
        contatosSuporte: 5,
        avaliacaoConteudo: 1.0,
        metodoPagamento: "boleto",
        dispositivoPrincipal: "mobile"
      }) {
        previsao
        probabilidade
        riscoAlto
      }
    }
    """
    r = requests.post(f"{BASE_URL}/graphql", json={'query': query})
    data = r.json()['data']['analiseChurn']
    
    if data['riscoAlto'] == True:
        log(f"Previsão Correta: Risco Alto ({data['probabilidade']:.2f})", "SUCCESS")
    else:
        log(f"Alerta: Modelo não detectou risco em perfil ruim. Prob: {data['probabilidade']}", "WARN")

def test_batch_upload():
    log("Testando Upload Batch (Gerando CSV em memória)...")
    # Criar CSV fake
    csv_content = """idade,tempo_assinatura_meses,plano_assinatura,valor_mensal,visualizacoes_mes,tempo_medio_sessao_min,contatos_suporte,avaliacao_conteudo,metodo_pagamento,dispositivo_principal
30,12,Basico,29.90,20,60,0,5.0,credito,mobile
40,1,Premium,99.90,0,5,10,1.0,boleto,mobile"""
    
    files = {'file': ('test.csv', csv_content, 'text/csv')}
    
    r = requests.post(f"{BASE_URL}/predict/batch", files=files)
    
    if r.status_code == 200:
        # Verificar se voltou CSV
        result_content = r.content.decode('utf-8')
        if "previsao_churn" in result_content:
            lines = result_content.strip().split('\n')
            log(f"Batch Processado com Sucesso. Linhas retornadas: {len(lines)-1}", "SUCCESS")
        else:
            log("Batch falhou: CSV retornado inválido", "FAIL")
    else:
        log(f"Erro no Upload Batch: {r.status_code} - {r.text}", "FAIL")

if __name__ == "__main__":
    print("\n🚀 INICIANDO TESTE PONTA A PONTA (E2E) 🚀\n")
    test_health()
    test_graphql_stats()
    test_graphql_simulation()
    test_batch_upload()
    print("\n✨ TESTE FINALIZADO ✨")
