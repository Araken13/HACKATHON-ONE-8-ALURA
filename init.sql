-- Criação da Tabela com constraints profissionais
CREATE TABLE IF NOT EXISTS historico_previsoes (
    id SERIAL PRIMARY KEY,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cliente_input JSONB, -- JSONB é mais performático para query no Postgres
    previsao VARCHAR(50),
    probabilidade FLOAT,
    risco_alto BOOLEAN
);

-- Indexação para performance (ex: buscar previsões de alto risco rapidamente)
CREATE INDEX IF NOT EXISTS idx_risco_alto ON historico_previsoes(risco_alto);
CREATE INDEX IF NOT EXISTS idx_data_hora ON historico_previsoes(data_hora);

-- TRIGGER: Função para garantir updated_at (simulação de log de auditoria)
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.data_hora = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- TRIGGER: Disparar a função antes de update (embora nosso app só faça insert, deixamos preparado)
DROP TRIGGER IF EXISTS trigger_update_timestamp ON historico_previsoes;
CREATE TRIGGER trigger_update_timestamp
    BEFORE UPDATE ON historico_previsoes
    FOR EACH ROW
    EXECUTE PROCEDURE update_timestamp();

-- POLICY (Row Level Security): Simulação de segurança
-- Em um app real multi-tenant, aqui limitaríamos o acesso por usuario_id
ALTER TABLE historico_previsoes ENABLE ROW LEVEL SECURITY;

-- Política permissiva para o user 'admin' (nosso app)
CREATE POLICY admin_all_access ON historico_previsoes
    FOR ALL
    TO PUBLIC
    USING (true);
