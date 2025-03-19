# database.py
# Configuração e conexão com o banco de dados

# Importação do SQLAlchemy para ORM
from sqlalchemy import create_engine
# Importação do sessionmaker para criar sessões do banco de dados
from sqlalchemy.ext.declarative import declarative_base
# Importação do sessionmaker para criar sessões do banco de dados
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco de dados SQLite
# Pode ser substituída por outro banco de dados como PostgreSQL ou MySQL
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

# Cria o motor de conexão com o banco de dados
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria uma fábrica de sessões para o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os modelos de dados
Base = declarative_base()