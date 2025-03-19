from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

# Importe seus módulos existentes
import crud, models, schemas
from database import SessionLocal, engine

# Criação das tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuração do CORS para permitir acesso do frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para desenvolvimento local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração JWT simplificada
SECRET_KEY = "dev_secret_key"  # Isso é apenas para desenvolvimento!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependency para obter DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Funções JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

# Endpoint para login
@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Obtém o usuário pelo email
    user = crud.get_user_by_email(db, email=form_data.username)
    
    # Verifica a senha
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Cria o token de acesso
    access_token = create_access_token(data={"sub": user.email})
    
    # Retorna o token e informações do usuário
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.id
    }

# Endpoint para criar usuário (registro)
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se o email já está cadastrado
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Cria o usuário
    return crud.create_user(db=db, user=user)

# Endpoint para obter informações do usuário por ID
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Busca o usuário
    db_user = crud.get_user(db, user_id=user_id)
    
    # Verifica se o usuário existe
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Por segurança básica: um usuário só pode ver seus próprios dados
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Não autorizado")
    
    return db_user

# Endpoint para obter o usuário atual
@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user