import strawberry
from typing import List, Optional
import joblib
import pandas as pd
import json
from database import SessionLocal, HistoricoPrevisao
import sys
from processing import preprocess_input  # Import corrigido!

# Tentar importar a classe Mock se necessária e disponibilizar no __main__
try:
    from train_model import MockChurnModel
    # Truque para o pickle achar a classe se ela foi salva no __main__
    sys.modules['__main__'].MockChurnModel = MockChurnModel
except ImportError:
    pass

# Carregar modelo (Singleton simplificado)
try:
    model = joblib.load('churn_model.joblib')
except:
    model = None

# --- Tipos GraphQL ---

@strawberry.type
class ChurnPrediction:
    previsao: str
    probabilidade: float
    risco_alto: bool
    cenario_analisado: str

@strawberry.type
class ChurnStats:
    total_analisados: int
    total_churn_previsto: int
    taxa_risco_percentual: float

# --- Inputs ---

@strawberry.input
class ClienteInputGQL:
    idade: int
    tempo_assinatura_meses: int
    plano_assinatura: str
    valor_mensal: float
    visualizacoes_mes: int
    tempo_medio_sessao_min: int
    contatos_suporte: int
    avaliacao_conteudo: float
    metodo_pagamento: str
    dispositivo_principal: str

# --- Resoluções (Resolvers) ---

def get_stats() -> ChurnStats:
    db = SessionLocal()
    try:
        total = db.query(HistoricoPrevisao).count()
        churn = db.query(HistoricoPrevisao).filter(HistoricoPrevisao.previsao == 'Vai cancelar').count()
        taxa = (churn / total * 100) if total > 0 else 0.0
        return ChurnStats(
            total_analisados=total, 
            total_churn_previsto=churn, 
            taxa_risco_percentual=round(taxa, 2)
        )
    finally:
        db.close()

def simulate_scenario(cliente: ClienteInputGQL, variacao_preco: Optional[float] = 0.0) -> ChurnPrediction:
    """
    Simula um cenário: E se mudarmos o preço? E se o cliente envelhecer?
    """
    if not model:
        return ChurnPrediction(previsao="Erro", probabilidade=0.0, risco_alto=False, cenario_analisado="Modelo Offline")

    # Converter input strawberry para dict
    data = {
        "idade": cliente.idade,
        "tempo_assinatura_meses": cliente.tempo_assinatura_meses,
        "plano_assinatura": cliente.plano_assinatura,
        "valor_mensal": cliente.valor_mensal + variacao_preco, # Aplica cenário
        "visualizacoes_mes": cliente.visualizacoes_mes,
        "tempo_medio_sessao_min": cliente.tempo_medio_sessao_min,
        "contatos_suporte": cliente.contatos_suporte,
        "avaliacao_conteudo": cliente.avaliacao_conteudo,
        "metodo_pagamento": cliente.metodo_pagamento,
        "dispositivo_principal": cliente.dispositivo_principal
    }

    # Pipeline de previsão
    df = pd.DataFrame([data])
    df_processed = preprocess_input(df)
    
    # Predict
    prob = 0.0
    if hasattr(model, 'predict_proba'):
        prob = float(model.predict_proba(df_processed)[0][1])
    
    pred_val = 1 if prob > 0.6 else 0 # Threshold do modelo
    
    texto_cenario = "Cenário Base"
    if variacao_preco != 0:
        texto_cenario = f"Simulação: Preço ajustado em {variacao_preco:+}"

    return ChurnPrediction(
        previsao="Vai cancelar" if pred_val == 1 else "Vai continuar",
        probabilidade=round(prob, 4),
        risco_alto=bool(prob > 0.6),
        cenario_analisado=texto_cenario
    )

# --- Definição da API ---

@strawberry.type
class Query:
    stats: ChurnStats = strawberry.field(resolver=get_stats)
    
    @strawberry.field
    def analise_churn(self, cliente: ClienteInputGQL) -> ChurnPrediction:
        return simulate_scenario(cliente, variacao_preco=0.0)

    @strawberry.field
    def simular_aumento_preco(self, cliente: ClienteInputGQL, aumento: float) -> ChurnPrediction:
        return simulate_scenario(cliente, variacao_preco=aumento)

schema = strawberry.Schema(query=Query)
