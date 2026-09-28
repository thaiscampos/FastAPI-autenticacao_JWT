from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(prefix='/auth', tags=['auth'])

def criar_token(usuario_id, duracao_token= timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = { "sub": str(usuario_id), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
   
    return jwt_codificado

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    print(usuario)
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return {'Senha incorreta'}
    return usuario



@auth_router.get('/')
async def autenticar():
    return {"message": "Authentication route"}



@auth_router.post('/criar_conta')  # Define a rota de cadastro
async def criar_conta(usuario_schema: UsuarioSchema,  # Recebe os dados
    session: Session = Depends(pegar_sessao)):  # Obtém a sessão

    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()  # Busca o usuário
    
    if usuario:  # Verifica se já existe
        raise HTTPException(status_code=400, detail=f"Email já cadastrado {usuario_schema.email}")  # Retorna erro
    else:  # Caso não exista
        nova_senha = bcrypt_context.hash(usuario_schema.senha)  # Criptografa a senha
        novo_usuario = Usuario(nome=usuario_schema.nome, email=usuario_schema.email, senha=nova_senha, admin=usuario_schema.admin, ativo=usuario_schema.ativo)  # Cria o usuário
        session.add(novo_usuario)  # Adiciona à sessão
        session.commit()  # Salva no banco
        return {"message": f"Conta criada com sucesso {usuario_schema.email}"}  # Retorna mensagem


# login -> email e senha -> token JWT(Json Web Token) 
 
@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session )
    
    if not usuario:
        raise HTTPException(status_code=400, detail='Usuario nao encontrado ou credenciais inválidas')
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7) )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
                }

@auth_router.post('/login-form')
async def login_form(dado_fromulario:OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dado_fromulario.username, dado_fromulario.password  , session )
    
    if not usuario:
        raise HTTPException(status_code=400, detail='Usuario nao encontrado ou credenciais inválidas')
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7) )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
                }

@auth_router.get('/refresh')
async def use_refresh_token(usuario: Usuario = Depends(verificar_token) ):
    #verificar o token
    access_token = criar_token(usuario.id)
    return {
            "access_token": access_token,
           
            "token_type": "Bearer"
                }

@auth_router.delete('/delete')
async def deletar_conta(id_usuario: int, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    
    session.delete(usuario)
    session.commit()
    
    return {"message": f"Conta deletada com sucesso {usuario.email}"}
   