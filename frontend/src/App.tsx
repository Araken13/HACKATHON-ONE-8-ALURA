import { useState } from 'react'
import { useQuery, gql, useLazyQuery } from '@apollo/client'
import Sandbox from './Sandbox'

// Queries GraphQL
const GET_STATS = gql`
  query GetStats {
    stats {
      totalAnalisados
      totalChurnPrevisto
      taxaRiscoPercentual
    }
  }
`

const ANALYZE_SCENARIO = gql`
  query Analyze($cliente: ClienteInputGQL!) {
    analiseChurn(cliente: $cliente) {
      previsao
      probabilidade
      riscoAlto
      cenarioAnalisado
    }
  }
`

function App() {
    // Estado para Stats
    const { data: statsData, loading: statsLoading, refetch: refetchStats } = useQuery(GET_STATS, {
        pollInterval: 5000 // Atualiza a cada 5s
    })

    // Estado para Simulador
    const [formData, setFormData] = useState({
        idade: 30,
        tempoAssinaturaMeses: 12,
        planoAssinatura: "padrao",
        valorMensal: 29.90,
        visualizacoesMes: 20,
        tempoMedioSessaoMin: 45,
        contatosSuporte: 0,
        avaliacaoConteudo: 4.0,
        metodoPagamento: "credito",
        dispositivoPrincipal: "mobile"
    })

    const [analyze, { data: simData, loading: simLoading }] = useLazyQuery(ANALYZE_SCENARIO)

    const handleSimulate = (e: React.FormEvent) => {
        e.preventDefault()
        analyze({ variables: { cliente: formData } })
    }

    // Estado para Upload
    const [uploading, setUploading] = useState(false)
    const [uploadMsg, setUploadMsg] = useState("")

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files) return
        const file = e.target.files[0]

        const formData = new FormData()
        formData.append('file', file)

        setUploading(true)
        setUploadMsg("Enviando...")

        try {
            const response = await fetch('http://127.0.0.1:8000/predict/batch', {
                method: 'POST',
                body: formData,
            })

            if (response.ok) {
                // Download automático do CSV
                const blob = await response.blob()
                const url = window.URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url
                a.download = `resultado_${file.name}`
                a.click()
                setUploadMsg("✅ Processado com sucesso! Download iniciado.")
                refetchStats() // Atualiza os contadores
            } else {
                setUploadMsg("❌ Erro no processamento.")
            }
        } catch (err) {
            setUploadMsg("❌ Erro de conexão.")
        } finally {
            setUploading(false)
        }
    }

    return (
        <div className="container">
            <header>
                <div className="logo">ChurnInsight 🔮</div>
                <div style={{ marginLeft: 'auto', fontSize: '0.9rem', color: '#94a3b8' }}>
                    Ambiente: Fase 2 (React + GraphQL + Sandbox)
                </div>
            </header>

            {/* DASHBOARD KPI */}
            <section className="grid">
                <div className="card">
                    <div className="stat-label">Total Analisado</div>
                    <div className="stat-value">
                        {statsLoading ? "..." : statsData?.stats.totalAnalisados}
                    </div>
                </div>
                <div className="card">
                    <div className="stat-label">Risco Previsto</div>
                    <div className="stat-value high-risk">
                        {statsLoading ? "..." : statsData?.stats.totalChurnPrevisto}
                    </div>
                    <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Clientes em Perigo</div>
                </div>
                <div className="card">
                    <div className="stat-label">Taxa de Churn</div>
                    <div className="stat-value">
                        {statsLoading ? "..." : statsData?.stats.taxaRiscoPercentual}%
                    </div>
                </div>
            </section>

            <div className="grid" style={{ gridTemplateColumns: '1fr 1fr' }}>

                {/* SIMULADOR */}
                <div className="card">
                    <h3>⚡ Simulador de Cenários</h3>
                    <form onSubmit={handleSimulate}>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                            <div>
                                <label>Idade</label>
                                <input type="number" value={formData.idade} onChange={e => setFormData({ ...formData, idade: +e.target.value })} />
                            </div>
                            <div>
                                <label>Mensalidade (R$)</label>
                                <input type="number" step="0.1" value={formData.valorMensal} onChange={e => setFormData({ ...formData, valorMensal: +e.target.value })} />
                            </div>
                            <div>
                                <label>Tempo Assinatura (Meses)</label>
                                <input type="number" value={formData.tempoAssinaturaMeses} onChange={e => setFormData({ ...formData, tempoAssinaturaMeses: +e.target.value })} />
                            </div>
                            <div>
                                <label>Visualizações (Mês)</label>
                                <input type="number" value={formData.visualizacoesMes} onChange={e => setFormData({ ...formData, visualizacoesMes: +e.target.value })} />
                            </div>
                            <div>
                                <label>Suporte (Chamados)</label>
                                <input type="number" value={formData.contatosSuporte} onChange={e => setFormData({ ...formData, contatosSuporte: +e.target.value })} />
                            </div>
                            <div>
                                <label>Avaliação (1-5)</label>
                                <input type="number" step="0.1" value={formData.avaliacaoConteudo} onChange={e => setFormData({ ...formData, avaliacaoConteudo: +e.target.value })} />
                            </div>
                        </div>
                        <button type="submit" disabled={simLoading}>
                            {simLoading ? "Calculando..." : "Simular Impacto"}
                        </button>
                    </form>

                    {simData && (
                        <div style={{ marginTop: '1.5rem', padding: '1rem', backgroundColor: simData.analiseChurn.riscoAlto ? 'rgba(239, 68, 68, 0.1)' : 'rgba(34, 197, 94, 0.1)', borderRadius: '8px', border: simData.analiseChurn.riscoAlto ? '1px solid #ef4444' : '1px solid #22c55e' }}>
                            <div style={{ fontWeight: 'bold', fontSize: '1.2rem', color: simData.analiseChurn.riscoAlto ? '#ef4444' : '#22c55e' }}>
                                {simData.analiseChurn.previsao}
                            </div>
                            <div>Probabilidade: <strong>{(simData.analiseChurn.probabilidade * 100).toFixed(1)}%</strong></div>
                            <div style={{ fontSize: '0.8rem', opacity: 0.7 }}>{simData.analiseChurn.cenarioAnalisado}</div>
                        </div>
                    )}
                </div>

                {/* BATCH UPLOAD */}
                <div className="card">
                    <h3>📂 Processamento em Lote</h3>
                    <p style={{ color: '#94a3b8', marginBottom: '2rem' }}>
                        Envie um arquivo CSV com milhares de clientes. O sistema processará tudo e retornará o arquivo preenchido com as previsões.
                    </p>

                    <label className="upload-area">
                        <input type="file" accept=".csv" hidden onChange={handleFileUpload} />
                        <span style={{ fontSize: '1.2rem', display: 'block', marginBottom: '0.5rem' }}>
                            {uploading ? "Processando..." : "Clique para selecionar CSV"}
                        </span>
                        <span style={{ fontSize: '0.9rem', color: '#94a3b8' }}>
                            {uploadMsg || "Suporta arquivos grandes"}
                        </span>
                    </label>
                </div>

            </div>

            {/* SANDBOX SECTION */}
            <Sandbox />

        </div>
    )
}

export default App
