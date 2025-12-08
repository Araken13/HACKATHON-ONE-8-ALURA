import joblib
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os
import json

# Adicionar caminho local para importar dependências do treino se necessário
sys.path.append(os.getcwd())

# Tentar importar a classe Mock se necessária
try:
    from train_model import MockChurnModel
except ImportError:
    pass

app = FastAPI(title="ChurnInsight API", description="API para previsão de Churn de clientes de Streaming")

# Carregar o modelo e os metadados (dicionário de tradução)
try:
    model = joblib.load('churn_model.joblib')
    with open('model_metadata.json', 'r') as f:
        metadata = json.load(f)
        
    # Inverter o mapeamento: O json tem { "0": "basico" }, nós queremos { "basico": 0 }
    mappings = metadata.get('mappings', {})
    reversed_mappings = {}
    
    for col, map_dict in mappings.items():
        # map_dict vem como chaves string do JSON, ex: "0", "1". Converter valores.
        # map_dict: { "0": "basico", "1": "padrao" }
        reversed_mappings[col] = {v: int(k) for k, v in map_dict.items()}
        
    print("Modelo e metadados carregados com sucesso!")
    print(f"Colunas categóricas mapeadas: {list(reversed_mappings.keys())}")

except Exception as e:
    print(f"ERRO CRÍTICO: Não foi possível carregar o modelo ou metadados. {e}")
    model = None
    reversed_mappings = {}

class ClienteInput(BaseModel):
    idade: int = 30
    tempo_assinatura_meses: int = 12
    plano_assinatura: str = "padrao"
    valor_mensal: float = 29.90
    visualizacoes_mes: int = 20
    tempo_medio_sessao_min: int = 60
    contatos_suporte: int = 1
    avaliacao_conteudo: float = 4.0
    metodo_pagamento: str = "credito"
    dispositivo_principal: str = "mobile"

@app.get("/")
def home():
    return {"status": "online", "mensagem": "API ChurnInsight operante."}

@app.post("/predict")
def predict_churn(cliente: ClienteInput):
    if not model:
        raise HTTPException(status_code=500, detail="Modelo não carregado no servidor.")

    try:
        # 1. Preparar os dados
        raw_data = cliente.dict()
        
        # 2. Pré-processamento (Igual ao Treino!)
        text_cols = ['plano_assinatura', 'metodo_pagamento', 'dispositivo_principal']
        
        # Lowercase e Strip
        for col in text_cols:
            if col in raw_data:
                raw_data[col] = str(raw_data[col]).lower().strip()
                
                # Mapeamentos manuais de correção (igual treino)
                if col == 'plano_assinatura':
                    if raw_data[col] == 'básico': raw_data[col] = 'basico'
                    if raw_data[col] == 'padrão': raw_data[col] = 'padrao'
                if col == 'metodo_pagamento':
                    if raw_data[col] in ['cartão de crédito', 'cartao de credito']: 
                        raw_data[col] = 'credito'

        # 3. Aplicar Encoding (Texto -> Número)
        processed_data = raw_data.copy()
        
        for col, mapping in reversed_mappings.items():
            if col in processed_data:
                val = processed_data[col]
                if val in mapping:
                    processed_data[col] = mapping[val]
                else:
                    # Fallback: se vier algo novo (ex: "smart watch"), usa o valor mais comum '0' ou gera erro?
                    # Para MVP, vamos usar 0 (primeira categoria) pra não quebrar
                    print(f"AVISO: Valor '{val}' desconhecido para coluna '{col}'. Usando padrão 0.")
                    processed_data[col] = 0 

        # Converter para DataFrame
        df_input = pd.DataFrame([processed_data])
        
        # Garantir ordem das colunas (se o metadados tiver a lista)
        if 'columns' in metadata:
            # Filtrar colunas que o modelo espera (remove extras se houver)
            # e reordenar
            expected_cols = metadata['columns']
            # Preencher colunas faltantes com 0 se necessário
            for col in expected_cols:
                if col not in df_input.columns:
                    df_input[col] = 0
            df_input = df_input[expected_cols]

        # 4. Previsão
        prediction = model.predict(df_input)[0]
        
        probabilidade = 0.0
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba(df_input)
            probabilidade = float(probs[0][1])
            
        prediction_val = int(prediction)
        resultado = "Vai cancelar" if prediction_val == 1 else "Vai continuar"
        
        return {
            "cliente": raw_data,
            "previsao": resultado,
            "probabilidade_churn": probabilidade,
            "risco_alto": bool(probabilidade > 0.6)
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc() # Print no terminal do servidor pra gente ver
        raise HTTPException(status_code=400, detail=f"Erro no processamento: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
