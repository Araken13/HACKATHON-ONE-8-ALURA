import requests
import time
import os

# Configurações
URL = "http://127.0.0.1:8000/predict/batch"
INPUT_FILE = "dataset_churn_streaming_3000_registros.csv"
OUTPUT_FILE = "resultado_previsoes_batch.csv"

def testar_batch():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Erro: Arquivo de entrada '{INPUT_FILE}' não encontrado.")
        return

    print(f"📡 Enviando '{INPUT_FILE}' para a API...")
    print("⏳ Aguarde o processamento...")
    
    start_time = time.time()
    
    try:
        with open(INPUT_FILE, 'rb') as f:
            files = {'file': (INPUT_FILE, f, 'text/csv')}
            response = requests.post(URL, files=files, stream=True)
            
            if response.status_code == 200:
                # Salvar o arquivo de resposta
                with open(OUTPUT_FILE, 'wb') as out:
                    for chunk in response.iter_content(chunk_size=8192):
                        out.write(chunk)
                
                duration = time.time() - start_time
                print(f"\n✅ SUCESSO! Processamento concluído em {duration:.2f} segundos.")
                print(f"📂 Arquivo salvo em: {os.path.abspath(OUTPUT_FILE)}")
                
                # Mostrar prévia
                print("\n--- Primeiras 3 linhas do resultado ---")
                with open(OUTPUT_FILE, 'r', encoding='utf-8') as res:
                    for _ in range(3):
                        print(res.readline().strip())
            else:
                print(f"❌ Erro na API: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"❌ Falha na conexão: {e}")
        print("💡 Dica: Verifique se a API está rodando no WSL (python api.py).")

if __name__ == "__main__":
    testar_batch()
