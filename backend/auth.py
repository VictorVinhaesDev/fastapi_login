# auth.py
# Arquivo para autenticação e segurança

# Importa os módulos necessários para autenticação
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

# Importa nossos módulos
import models, schemas
from database import get_db

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações de segurança obtidas do arquivo .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Verifica se SECRET_KEY está definida
if not SECRET_KEY:
    raise ValueError("A variável de ambiente SECRET_KEY não está definida. Verifique seu arquivo .env")

# Contexto para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de autenticação OAuth2 (para o botão "Authorize" no Swagger)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scheme_name="JWT"
)

# Função para verificar senha
def verify_password(plain_password, hashed_password):
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.
    
    Args:
        plain_password: Senha em texto plano
        hashed_password: Hash da senha armazenada
    
    Returns:
        True se a senha estiver correta, False caso contrário
    """
    return pwd_context.verify(plain_password, hashed_password)

# Função para gerar hash de senha
def get_password_hash(password):
    """
    Gera um hash seguro para a senha.
    
    Args:
        password: Senha em texto plano
    
    Returns:
        Hash da senha
    """
    return pwd_context.hash(password)

# Função para criar um token de acesso
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Cria um token JWT de acesso.
    
    Args:
        data: Dados a serem codificados no token
        expires_delta: Tempo de expiração do token
    
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    
    # Define o tempo de expiração
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Adiciona o tempo de expiração aos dados do token
    to_encode.update({"exp": expire})
    
    # Codifica o token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

# Função para obter o usuário atual a partir do token
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Obtém o usuário atual a partir do token JWT.
    
    Args:
        token: Token JWT
        db: Sessão do banco de dados
    
    Returns:
        Usuário atual
    
    Raises:
        HTTPException: Se o token for inválido ou o usuário não for encontrado
    """
    # Define a exceção para credenciais inválidas
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodifica o token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    # Busca o usuário pelo email
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    
    if user is None:
        raise credentials_exception
    
    return user

