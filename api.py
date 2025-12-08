import joblib
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# Adicionar caminho local para importar dependências do treino se necessário
sys.path.append(os.getcwd())

# Tentar importar a classe Mock se necessária (para o pickle funcionar)
try:
    from train_model import MockChurnModel
except ImportError:
    pass

app = FastAPI(title="ChurnInsight API", description="API para previsão de Churn de clientes de Streaming")

# Carregar o modelo na inicialização
try:
    model = joblib.load('churn_model.joblib')
    # Carregar metadados para garantir integridade das colunas
    # (Em produção real lemos o json, aqui vamos simplificar garantindo o contrato)
    print("Modelo carregado com sucesso via joblib!")
except Exception as e:
    print(f"ERRO CRÍTICO: Não foi possível carregar o modelo. {e}")
    model = None

# Definir o contrato de entrada (JSON)
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
    return {"status": "online", "mensagem": "API ChurnInsight operante. Use /predict para previsões."}

@app.post("/predict")
def predict_churn(cliente: ClienteInput):
    if not model:
        raise HTTPException(status_code=500, detail="Modelo não carregado no servidor.")

    # Converter entrada para DataFrame
    data = {
        "idade": [cliente.idade],
        "tempo_assinatura_meses": [cliente.tempo_assinatura_meses],
        "plano_assinatura": [cliente.plano_assinatura],
        "valor_mensal": [cliente.valor_mensal],
        "visualizacoes_mes": [cliente.visualizacoes_mes],
        "tempo_medio_sessao_min": [cliente.tempo_medio_sessao_min],
        "contatos_suporte": [cliente.contatos_suporte],
        "avaliacao_conteudo": [cliente.avaliacao_conteudo],
        "metodo_pagamento": [cliente.metodo_pagamento],
        "dispositivo_principal": [cliente.dispositivo_principal]
    }
    
    df_input = pd.DataFrame(data)
    
    try:
        # Fazer a previsão
        prediction = model.predict(df_input)[0]
        
        # Tentar obter probabilidade
        probabilidade = 0.0
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba(df_input)
            # Probabilidade da classe 1 (Churn) - garantir float python
            probabilidade = float(probs[0][1])
            
        prediction_val = int(prediction) # garantir int python
        resultado = "Vai cancelar" if prediction_val == 1 else "Vai continuar"
        
        # Converter dados de entrada para dicionário limpo (sem numpy)
        # df_input.to_dict('records')[0] já converte bem
        cliente_dict = df_input.to_dict(orient='records')[0]
        
        return {
            "cliente": cliente_dict,
            "previsao": resultado,
            "probabilidade_churn": probabilidade,
            "risco_alto": bool(probabilidade > 0.6) # garantir bool python
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro no processamento do modelo: {str(e)}")

if __name__ == "__main__":
    # Rodar servidor
    uvicorn.run(app, host="127.0.0.1", port=8000)
