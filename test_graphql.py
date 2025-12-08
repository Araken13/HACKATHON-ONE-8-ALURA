import requests

URL = "http://127.0.0.1:8000/graphql"

# Consulta (Query) que vamos enviar
QUERY = """
query {
  stats {
    totalAnalisados
    taxaRiscoPercentual
  }
  
  simulacao: analiseChurn(cliente: {
    idade: 30,
    tempoAssinaturaMeses: 12,
    planoAssinatura: "padrao",
    valorMensal: 29.90,
    visualizacoesMes: 20,
    tempoMedioSessaoMin: 60,
    contatosSuporte: 0,
    avaliacaoConteudo: 5.0,
    metodoPagamento: "credito",
    dispositivoPrincipal: "mobile"
  }) {
    previsao
    probabilidade
    cenarioAnalisado
  }
}
"""

def test_graphql():
    print("📡 Enviando Query GraphQL...")
    try:
        response = requests.post(URL, json={'query': QUERY})
        
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print("❌ Erro na Query:", data["errors"])
            else:
                print("✅ SUCESSO! Resposta do GraphQL:")
                print(data["data"])
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"❌ Falha na conexão: {e}")

if __name__ == "__main__":
    test_graphql()
