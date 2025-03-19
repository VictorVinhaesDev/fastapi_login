# models.py
# Definição dos modelos de dados para o banco de dados

# Importações do SQLAlchemy para definição dos modelos
from sqlalchemy import Boolean, Column, Integer, String, DateTime
# Importação de datetime para registrar datas
from sqlalchemy.sql import func
# Importação da classe Base do módulo de banco de dados
from database import Base

class User(Base):
    """
    Modelo de dados para a tabela de usuários no banco de dados.
    Define a estrutura da tabela e os tipos de dados para cada coluna.
    """
    # Nome da tabela no banco de dados
    __tablename__ = "users"

    # Colunas da tabela
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())