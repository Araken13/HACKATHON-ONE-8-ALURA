import React, { useState } from 'react';
import { Download, Database, Settings } from 'lucide-react';

const MLDataGenerator = () => {
  const [rows, setRows] = useState(10000);
  const [columns, setColumns] = useState({
    id: true,
    timestamp: true,
    valor: true,
    categoria: true,
    quantidade: true,
    status: true,
    regiao: true,
    score: true
  });
  const [generating, setGenerating] = useState(false);

  const categorias = ['A', 'B', 'C', 'D', 'E'];
  const status = ['Ativo', 'Inativo', 'Pendente', 'Concluído'];
  const regioes = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro'];

  const generateData = () => {
    setGenerating(true);
    
    setTimeout(() => {
      const data = [];
      const headers = [];
      
      if (columns.id) headers.push('id');
      if (columns.timestamp) headers.push('timestamp');
      if (columns.valor) headers.push('valor');
      if (columns.categoria) headers.push('categoria');
      if (columns.quantidade) headers.push('quantidade');
      if (columns.status) headers.push('status');
      if (columns.regiao) headers.push('regiao');
      if (columns.score) headers.push('score');
      
      data.push(headers.join(','));
      
      const startDate = new Date('2020-01-01');
      const endDate = new Date('2024-12-31');
      
      for (let i = 0; i < rows; i++) {
        const row = [];
        
        if (columns.id) row.push(i + 1);
        
        if (columns.timestamp) {
          const randomDate = new Date(
            startDate.getTime() + 
            Math.random() * (endDate.getTime() - startDate.getTime())
          );
          row.push(randomDate.toISOString());
        }
        
        if (columns.valor) {
          row.push((Math.random() * 10000).toFixed(2));
        }
        
        if (columns.categoria) {
          row.push(categorias[Math.floor(Math.random() * categorias.length)]);
        }
        
        if (columns.quantidade) {
          row.push(Math.floor(Math.random() * 1000));
        }
        
        if (columns.status) {
          row.push(status[Math.floor(Math.random() * status.length)]);
        }
        
        if (columns.regiao) {
          row.push(regioes[Math.floor(Math.random() * regioes.length)]);
        }
        
        if (columns.score) {
          row.push((Math.random() * 100).toFixed(2));
        }
        
        data.push(row.join(','));
      }
      
      const csvContent = data.join('\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      
      link.setAttribute('href', url);
      link.setAttribute('download', `ml_dataset_${rows}_rows.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      setGenerating(false);
    }, 100);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="flex items-center gap-3 mb-6">
            <Database className="w-8 h-8 text-indigo-600" />
            <h1 className="text-3xl font-bold text-gray-800">
              Gerador de Dados para ML
            </h1>
          </div>
          
          <div className="mb-8">
            <p className="text-gray-600">
              Configure e gere um dataset CSV com grandes volumes de dados simulados
              para treinar seu modelo de Machine Learning.
            </p>
          </div>

          <div className="bg-indigo-50 rounded-lg p-6 mb-6">
            <div className="flex items-center gap-2 mb-4">
              <Settings className="w-5 h-5 text-indigo-600" />
              <h2 className="text-xl font-semibold text-gray-800">Configurações</h2>
            </div>
            
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Número de Linhas: {rows.toLocaleString('pt-BR')}
              </label>
              <input
                type="range"
                min="1000"
                max="1000000"
                step="1000"
                value={rows}
                onChange={(e) => setRows(parseInt(e.target.value))}
                className="w-full h-2 bg-indigo-200 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>1.000</span>
                <span>1.000.000</span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Colunas a Incluir:
              </label>
              <div className="grid grid-cols-2 gap-3">
                {Object.keys(columns).map((col) => (
                  <label key={col} className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={columns[col]}
                      onChange={(e) => setColumns({...columns, [col]: e.target.checked})}
                      className="w-4 h-4 text-indigo-600 rounded"
                    />
                    <span className="text-sm text-gray-700 capitalize">{col}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>

          <div className="bg-gray-50 rounded-lg p-6 mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">
              Estrutura do Dataset:
            </h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li><strong>id:</strong> Identificador único sequencial</li>
              <li><strong>timestamp:</strong> Data/hora aleatória entre 2020-2024</li>
              <li><strong>valor:</strong> Valores numéricos entre 0 e 10.000</li>
              <li><strong>categoria:</strong> Categorias A, B, C, D, E</li>
              <li><strong>quantidade:</strong> Valores inteiros entre 0 e 1.000</li>
              <li><strong>status:</strong> Ativo, Inativo, Pendente, Concluído</li>
              <li><strong>regiao:</strong> Norte, Sul, Leste, Oeste, Centro</li>
              <li><strong>score:</strong> Pontuação entre 0 e 100</li>
            </ul>
          </div>

          <button
            onClick={generateData}
            disabled={generating || Object.values(columns).every(v => !v)}
            className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-semibold py-4 px-6 rounded-lg flex items-center justify-center gap-3 transition-colors"
          >
            <Download className="w-5 h-5" />
            {generating ? 'Gerando...' : `Gerar e Baixar CSV (${rows.toLocaleString('pt-BR')} linhas)`}
          </button>

          <p className="text-xs text-gray-500 text-center mt-4">
            O arquivo será baixado automaticamente quando a geração for concluída
          </p>
        </div>
      </div>
    </div>
  );
};

export default MLDataGenerator;