from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from models import Pedido, Usuario, ItemPedido

order_router = APIRouter(prefix='/orders', tags=['pedidos'], dependencies=[Depends(verificar_token)])

@order_router.get('/')
async def pedidos():
    return {"message": "List of orders"}


@order_router.post('/pedidos')
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"message": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}


@order_router.post('/pedido/cancelar/{id_pedido}')
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido =  session.query(Pedido).filter(Pedido.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido não encontrado')
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=400, detail='Voce nao tem autorização para fazer essa modificação')
    
    pedido.status = 'CANCELADO'
    status_pedido  = {'mensagem': f"pedido: {id_pedido} cancelado com sucesso", "pedido": pedido}
    session.commit()
   
    return status_pedido

@order_router.get('/listar')
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario  = Depends(verificar_token)):
    
    if not usuario.admin:
        print(usuario)
        print(usuario.admin)
        raise HTTPException(
        status_code=403,
        detail="Você não tem autorização para acessar esta rota"
        )
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }


@order_router.post('/pedido/adicionar-item/{id_pedido}')
async def adcionar_item(id_pedido: int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario  = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=400,
        detail="Pedido nao encontrado")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorização")
    
    item_pedido = ItemPedido(id_pedido, item_pedido_schema.sabor, item_pedido_schema.quantidade, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario)
    
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": 'Item criado com sucesso',
        'item_id': item_pedido.id,
        'preco_pedido': pedido.preco
}
    
    

@order_router.delete('/deletar_item')  # Define a rota de exclusão

async def deletar_item(
    id_item: int,  # Recebe o ID do item
    usuario: Usuario = Depends(verificar_token),  # Verifica o usuário
    session: Session = Depends(pegar_sessao)  # Obtém a sessão
):

    item = session.query(ItemPedido).filter(
        ItemPedido.id == id_item
    ).first()  # Busca o item pelo ID

    if not item:  # Verifica se o item existe
        raise HTTPException(
            status_code=404,
            detail="Item não encontrado"
        )

    session.delete(item)  # Remove o item

    session.commit()  # Salva a alteração

    return {
        "message": f"Item deletado com sucesso: {id_item}"
    }


@order_router.post('/pedido/remover-item/{item_pedido}')
async def adcionar_item(item_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario  = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    
    if not item_pedido:
        raise HTTPException(status_code=400,
        detail="Item nao encontrado")
    elif not usuario.admin and usuario.id != item_pedido.pedido.usuario:
        raise HTTPException(status_code=401, detail="Voce nao tem autorização")
    
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": 'Item removido com sucesso',
        'quantidade de iten pedidos': len(pedido.itens),
        'pedido': pedido
}


#finalizar um pedido

@order_router.post('/pedido/finalizar/{id_pedido}')
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido =  session.query(Pedido).filter(Pedido.id == id_pedido).first()
    
    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido não encontrado')
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=400, detail='Voce nao tem autorização para fazer essa modificação')
    
    pedido.status = 'FINALIZADO'
    status_pedido  = {'mensagem': f"pedido: {pedido.id} finalizado com sucesso", "pedido": pedido}
    session.commit()
   
    return status_pedido

#visualizar 1 pedido
@order_router.get('/pedido/{id_pedido}', )
async def visualizar_pedido(id_pedido: int, session:Session = Depends(pegar_sessao), usuario:Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido não encontrado')
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail='Voce não tem autorização')
    return {
        'quantidade de itens': len(pedido.itens),
        'pedido': pedido
    }

    


#visualizar todos os pedidos de 1 usuario
@order_router.get('/listar/pedidos-usuario', response_model=List[ResponsePedidoSchema])
async def listar_pedido_usuario(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    return pedidos
