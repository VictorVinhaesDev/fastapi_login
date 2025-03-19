# schemas.py
# Definição dos schemas Pydantic para validação de dados

# Importação do Pydantic para validação de dados
from pydantic import BaseModel, EmailStr, Field
# Importação do datetime para tipagem de datas
from datetime import datetime
# Importação do typing para uso de Optional
from typing import Optional

class UserBase(BaseModel):
    """
    Schema base para usuários, contendo campos comuns a todos os schemas de usuário.
    """
    email: EmailStr = Field(..., description="Email do usuário (único)")


class UserCreate(UserBase):
    """
    Schema para criação de usuário, que inclui a senha.
    """
    password: str = Field(..., min_length=8, description="Senha do usuário (mínimo 8 caracteres)")


class UserUpdate(BaseModel):
    """
    Schema para atualização de usuário, com todos os campos opcionais.
    """
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, description="Nova senha (mínimo 8 caracteres)")
    is_active: Optional[bool] = None


class User(UserBase):
    """
    Schema para representação de usuário, sem incluir a senha.
    Usado para retornar dados de usuário nas respostas da API.
    """
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """
        Configuração do Pydantic para permitir leitura de modelos ORM.
        """
        orm_mode = True