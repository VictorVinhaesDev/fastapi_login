# crud.py
# Operações de CRUD (Create, Read, Update, Delete) para usuários

# Importação do SQLAlchemy para operações com o banco de dados
from sqlalchemy.orm import Session
# Importação dos módulos internos da aplicação
import models, schemas
# Importação do passlib para hash de senhas
from passlib.context import CryptContext

# Configuração do contexto de criptografia para senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Função para criar um hash seguro da senha.
    
    Args:
        password: A senha em texto plano
        
    Returns:
        O hash da senha
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Função para verificar se uma senha em texto plano corresponde ao hash armazenado.
    
    Args:
        plain_password: A senha em texto plano
        hashed_password: O hash da senha armazenado
        
    Returns:
        True se a senha corresponder ao hash, False caso contrário
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, user_id: int):
    """
    Busca um usuário pelo ID.
    
    Args:
        db: Sessão do banco de dados
        user_id: ID do usuário a ser buscado
        
    Returns:
        O usuário encontrado ou None
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """
    Busca um usuário pelo email.
    
    Args:
        db: Sessão do banco de dados
        email: Email do usuário a ser buscado
        
    Returns:
        O usuário encontrado ou None
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Lista todos os usuários com suporte a paginação.
    
    Args:
        db: Sessão do banco de dados
        skip: Quantidade de registros a pular (para paginação)
        limit: Limite de registros a retornar
        
    Returns:
        Lista de usuários
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Cria um novo usuário.
    
    Args:
        db: Sessão do banco de dados
        user: Dados do usuário a ser criado
        
    Returns:
        O usuário criado
    """
    # Cria o hash da senha antes de armazenar
    hashed_password = get_password_hash(user.password)
    
    # Cria uma instância do modelo User
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )
    
    # Adiciona o usuário à sessão e commit
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    """
    Atualiza um usuário existente.
    
    Args:
        db: Sessão do banco de dados
        user_id: ID do usuário a ser atualizado
        user: Novos dados do usuário
        
    Returns:
        O usuário atualizado
    """
    # Busca o usuário pelo ID
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    # Atualiza os campos que foram fornecidos
    update_data = user.dict(exclude_unset=True)
    
    # Se uma nova senha foi fornecida, faz o hash dela
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    # Atualiza os atributos do modelo
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    # Commit das alterações
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """
    Exclui um usuário pelo ID.
    
    Args:
        db: Sessão do banco de dados
        user_id: ID do usuário a ser excluído
        
    Returns:
        None
    """
    # Busca o usuário pelo ID
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    # Remove o usuário e commit
    db.delete(db_user)
    db.commit()