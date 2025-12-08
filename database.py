import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Configuração do Banco (Lê do ambiente ou usa SQLite local por padrão)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./churn_database.db")

# Ajuste para args do SQLite vs Postgres
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Modelo da Tabela (Schema)
class HistoricoPrevisao(Base):
    __tablename__ = "historico_previsoes"

    id = Column(Integer, primary_key=True, index=True)
    data_hora = Column(DateTime, default=datetime.utcnow)
    
    # Dados de Entrada (salvos como JSON para flexibilidade)
    cliente_input = Column(JSON)
    
    # Dados de Saída
    previsao = Column(String) # "Vai cancelar" / "Vai continuar"
    probabilidade = Column(Float)
    risco_alto = Column(Boolean)

# Função para criar as tabelas no banco (se não existirem)
def init_db():
    Base.metadata.create_all(bind=engine)
