import joblib
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import sys
import os
import io
import json

# Import GraphQL
import strawberry
from strawberry.fastapi import GraphQLRouter
from schema import schema

# Import Processing
from processing import preprocess_input

# Imports locais (Banco de Dados)
from database import SessionLocal, init_db, HistoricoPrevisao

# Adicionar caminho local para importar dependências
sys.path.append(os.getcwd())

# Tentar importar a classe Mock se necessária e disponibilizar no __main__
# (Correção crítica para o Joblib/Pickle achar a classe)
try:
    from train_model import MockChurnModel
    sys.modules['__main__'].MockChurnModel = MockChurnModel
except ImportError:
    pass

from fastapi.middleware.cors import CORSMiddleware

# --- Inicialização do App ---
app = FastAPI(title="ChurnInsight API", description="API para previsão de Churn de clientes de Streaming")

# Configurar CORS (Permitir acesso do Frontend React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique o domínio exato
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Rota GraphQL ---
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# --- Configuração de Banco de Dados ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicia Banco
init_db()

# --- Carregamento do Modelo ---
try:
    model = joblib.load('churn_model.joblib')
    print("Modelo carregado com sucesso!")
except Exception as e:
    print(f"ERRO CRÍTICO: Modelo não carregado. {e}")
    model = None

# --- Models Pydantic ---
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

# --- Endpoints REST ---

@app.get("/")
def home():
    return {"status": "online", "mensagem": "API ChurnInsight operante (REST + GraphQL)."}

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(HistoricoPrevisao).count()
    churn_count = db.query(HistoricoPrevisao).filter(HistoricoPrevisao.previsao == "Vai cancelar").count()
    taxa_churn = (churn_count / total * 100) if total > 0 else 0.0
    return {
        "total_analisados": total,
        "total_churn_previsto": churn_count,
        "taxa_risco_base": f"{taxa_churn:.1f}%"
    }

@app.post("/predict")
def predict_churn(cliente: ClienteInput, db: Session = Depends(get_db)):
    if not model:
        raise HTTPException(status_code=500, detail="Modelo não carregado.")

    try:
        raw_data = cliente.dict()
        df_raw = pd.DataFrame([raw_data])
        
        # Usar função importada do processing
        df_final = preprocess_input(df_raw)

        # Previsão
        prediction = model.predict(df_final)[0]
        probabilidade = 0.0
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba(df_final)
            probabilidade = float(probs[0][1])
            
        resultado = "Vai cancelar" if int(prediction) == 1 else "Vai continuar"
        risco = bool(probabilidade > 0.6)

        # Salvar no banco
        db.add(HistoricoPrevisao(
            cliente_input=raw_data,
            previsao=resultado,
            probabilidade=probabilidade,
            risco_alto=risco
        ))
        db.commit()
        
        return {
            "cliente": raw_data,
            "previsao": resultado,
            "probabilidade_churn": probabilidade,
            "risco_alto": risco
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Erro: {str(e)}")

@app.post("/predict/batch")
async def predict_batch(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Recebe um arquivo CSV, processa previsões em lote, salva no banco e retorna CSV preenchido."""
    if not model:
        raise HTTPException(status_code=500, detail="Modelo não carregado.")
        
    try:
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        
        df_processed = preprocess_input(df)
        
        predictions = model.predict(df_processed)
        df['previsao_churn'] = ["Vai cancelar" if p == 1 else "Vai continuar" for p in predictions]
        
        probs = []
        if hasattr(model, 'predict_proba'):
            raw_probs = model.predict_proba(df_processed)
            probs = [float(p[1]) for p in raw_probs]
        else:
            probs = [0.9 if p == 1 else 0.1 for p in predictions] # Fallback
            
        df['probabilidade'] = [round(p, 4) for p in probs]
        df['risco_alto'] = [bool(p > 0.6) for p in probs]

        # --- SALVAR NO BANCO ---
        batch_records = []
        for index, row in df.iterrows():
            # Extrair apenas input para o JSONB
            # Ignora as colunas de resultado que acabamos de adicionar para não duplicar no JSON
            input_cols = [c for c in row.index if c not in ['previsao_churn', 'probabilidade', 'risco_alto']]
            cliente_input = row[input_cols].to_dict()
            
            # Converter tipos numpy para python nativo (evita erro json)
            for k, v in cliente_input.items():
                if hasattr(v, 'item'): cliente_input[k] = v.item()

            record = HistoricoPrevisao(
                cliente_input=cliente_input,
                previsao=row['previsao_churn'],
                probabilidade=row['probabilidade'],
                risco_alto=row['risco_alto']
            )
            batch_records.append(record)
        
        # Bulk Insert (Mais rápido)
        db.add_all(batch_records)
        db.commit()
        # -----------------------
        
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=previsoes_churn.csv"
        return response

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Erro ao processar arquivo: {str(e)}")

if __name__ == "__main__":
    # Host 0.0.0.0 permite acesso externo (necessário para Docker)
    uvicorn.run(app, host="0.0.0.0", port=8000)
