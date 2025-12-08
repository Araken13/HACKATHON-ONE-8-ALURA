import joblib
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import sys
import os
import json

# Imports locais (Banco de Dados)
from database import SessionLocal, init_db, HistoricoPrevisao

# Adicionar caminho local para importar dependências do treino se necessário
sys.path.append(os.getcwd())

# Tentar importar a classe Mock se necessária
try:
    from train_model import MockChurnModel
except ImportError:
    pass

app = FastAPI(title="ChurnInsight API", description="API para previsão de Churn de clientes de Streaming")

# --- Configuração de Banco de Dados ---
# Dependência para obter sessão do banco a cada request (Padrão FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicializar tabelas ao arrancar
init_db()

# --- Carregamento do Modelo ---
# Carregar o modelo e os metadados (dicionário de tradução)
try:
    model = joblib.load('churn_model.joblib')
    with open('model_metadata.json', 'r') as f:
        metadata = json.load(f)
        
    # Inverter o mapeamento: O json tem { "0": "basico" }, nós queremos { "basico": 0 }
    mappings = metadata.get('mappings', {})
    reversed_mappings = {}
    
    for col, map_dict in mappings.items():
        reversed_mappings[col] = {v: int(k) for k, v in map_dict.items()}
        
    print("Modelo e metadados carregados com sucesso!")

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
    return {"status": "online", "mensagem": "API ChurnInsight operante com Persistência SQLite."}

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Retorna estatísticas baseadas no histórico de previsões"""
    total = db.query(HistoricoPrevisao).count()
    churn_count = db.query(HistoricoPrevisao).filter(HistoricoPrevisao.previsao == "Vai cancelar").count()
    
    taxa_churn = 0.0
    if total > 0:
        taxa_churn = (churn_count / total) * 100
        
    return {
        "total_analisados": total,
        "total_churn_previsto": churn_count,
        "taxa_risco_base": f"{taxa_churn:.1f}%"
    }

@app.post("/predict")
def predict_churn(cliente: ClienteInput, db: Session = Depends(get_db)):
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
                    processed_data[col] = 0 

        # Converter para DataFrame
        df_input = pd.DataFrame([processed_data])
        
        if 'columns' in metadata:
            expected_cols = metadata['columns']
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
        risco = bool(probabilidade > 0.6)

        # 5. SALVAR NO BANCO (Persistência)
        # Salvamos o raw_data (input original do cliente) para auditoria futura
        novo_registro = HistoricoPrevisao(
            cliente_input=raw_data,
            previsao=resultado,
            probabilidade=probabilidade,
            risco_alto=risco
        )
        db.add(novo_registro)
        db.commit()
        db.refresh(novo_registro)
        
        return {
            "id_analise": novo_registro.id,  # Retorna o ID do banco pra referência
            "cliente": raw_data,
            "previsao": resultado,
            "probabilidade_churn": probabilidade,
            "risco_alto": risco
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Erro no processamento: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
