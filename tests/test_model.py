import joblib
import pandas as pd
import json
import sys
import os

# Adicionar diretório atual ao path para importar a classe do arquivo train_model
sys.path.append(os.getcwd())

# Importar a classe para o pickle reconhecer
try:
    from train_model import MockChurnModel
except ImportError:
    print("Aviso: Não foi possível importar MockChurnModel de train_model. Necessário se o modelo salvo for dessa classe.")

def test_prediction():
    print("=== TESTE DE PREVISÃO DE CHURN ===")
    print("Carregando modelo e metadados...")
    try:
        model = joblib.load('churn_model.joblib')
        with open('model_metadata.json', 'r') as f:
            metadata = json.load(f)
    except FileNotFoundError:
        print("Erro: Artefatos do modelo não encontrados. Execute train_model.py primeiro.")
        return

    print("Modelo carregado com sucesso.")
    
    # Criar dados de teste (3 cenários distintos)
    test_cases = [
        {
            "id": "TEST_01",
            "idade": 30,
            "tempo_assinatura_meses": 24, # Longo prazo
            "plano_assinatura": "premium",
            "valor_mensal": 39.90,
            "visualizacoes_mes": 50,
            "tempo_medio_sessao_min": 60,
            "contatos_suporte": 0,
            "avaliacao_conteudo": 5.0, # Alta satisfação
            "metodo_pagamento": "credito",
            "dispositivo_principal": "mobile"
        },
        {
            "id": "TEST_02",
            "idade": 40,
            "tempo_assinatura_meses": 2, # Curto prazo (Risco)
            "plano_assinatura": "basico",
            "valor_mensal": 19.90,
            "visualizacoes_mes": 10,
            "tempo_medio_sessao_min": 15,
            "contatos_suporte": 5,
            "avaliacao_conteudo": 1.5, # Baixa satisfação (Risco)
            "metodo_pagamento": "boleto",
            "dispositivo_principal": "tv"
        },
        {
            "id": "TEST_03",
            "idade": 25,
            "tempo_assinatura_meses": 5, # Curto prazo
            "plano_assinatura": "padrao",
            "valor_mensal": 29.90,
            "visualizacoes_mes": 30,
            "tempo_medio_sessao_min": 45,
            "contatos_suporte": 2,
            "avaliacao_conteudo": 3.5, # Satisfação média
            "metodo_pagamento": "pix",
            "dispositivo_principal": "tablet"
        }
    ]
    
    df_test = pd.DataFrame(test_cases)
    
    print(f"\nTestando com {len(test_cases)} clientes simulados...")
    
    try:
        # Fazer previsão
        predictions = model.predict(df_test)
        
        # Tentar pegar probabilidades se o modelo suportar
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba(df_test)
        else:
            probs = [[0, 0]] * len(predictions)
        
        print("\n--- RESULTADOS ---")
        for i, (pred, prob) in enumerate(zip(predictions, probs)):
            cliente_id = test_cases[i]['id']
            churn_str = "⚠️ VAI CANCELAR" if pred == 1 else "✅ CLIENTE FIEL"
            chance = prob[1] * 100 if len(prob) > 1 else 0
            
            print(f"Cliente {cliente_id}: {churn_str}")
            print(f"   Probabilidade de Churn: {chance:.1f}%")
            print(f"   (Tempo: {test_cases[i]['tempo_assinatura_meses']} meses, Avaliação: {test_cases[i]['avaliacao_conteudo']})")
            print("-" * 30)
            
    except Exception as e:
        print(f"Erro Fatal na previsão: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_prediction()
