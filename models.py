from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType


# conexão com o banco de dados
db = create_engine("sqlite:///./banco.db")
#cria a base para os modelos
Base = declarative_base()

#cria as tabelas no banco de dados
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column('id',   Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String, nullable=False)
    email = Column('email', String, unique=True, nullable=False) 
    senha = Column('senha', String, nullable=False)  
    ativo = Column('ativo', Boolean, default=True)   
    admin = Column('admin',  Boolean, default=False)
    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
        
class Pedido(Base):
    __tablename__= 'pedidos'
   # STATUS_PEDIDOS  = (['Pendente', 'Pendente'], ['Pago', 'Pago'], ['Cancelado', 'Cancelado'])
    id = Column('id', Integer, primary_key=True, autoincrement=True)

    usuario = Column("usuario", Integer, ForeignKey('usuarios.id'), nullable=False)
    status = Column("status", String)
    preco = Column(
        "preco", Float, nullable=False)
    itens = relationship("ItemPedido", cascade='all, delete')
    
    def __init__(self, usuario, status = "Pendente", preco = 0.0):
        self.status = status
        self.usuario = usuario
        self.preco = preco
        
    def calcular_preco(self):
        print("Quantidade de itens:", len(self.itens))

        self.preco = 0

        for item in self.itens:
            subtotal = item.preco_unitario * item.quantidade

            print(
            f"Preço: {item.preco_unitario} | "
            f"Quantidade: {item.quantidade} | "
            f"Subtotal: {subtotal}"
        )

            self.preco += subtotal

        print("TOTAL:", self.preco)
        
        
class ItemPedido(Base):
    __tablename__= 'itens_pedidos'
    id = Column('id', Integer, primary_key=True, autoincrement=True)

    sabor = Column("sabor", String, nullable=False)
    quantidade = Column("quantidade", Integer, nullable=False)
    tamanho = Column("tamanho", String, nullable=False)
    preco_unitario = Column("preco_unitario", Float, nullable=False)
    pedido = Column("pedido", Integer, ForeignKey('pedidos.id'), nullable=False)
    def __init__(self, pedido, sabor, quantidade, tamanho, preco_unitario):
        self.pedido = pedido
        self.sabor = sabor
        self.quantidade = quantidade
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
#executa a criação das tabelas no banco de dados
