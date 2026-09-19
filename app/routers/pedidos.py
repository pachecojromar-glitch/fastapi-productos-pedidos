from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import obtener_sesion
from app.models import Pedido, PedidoCrear, PedidoActualizar, PedidoLectura, PedidoConTotal, Producto

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", response_model=PedidoLectura, status_code=status.HTTP_201_CREATED)
def crear_pedido(pedido: PedidoCrear, session: Session = Depends(obtener_sesion)):
    producto = session.get(Producto, pedido.producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if producto.stock < pedido.cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    db_pedido = Pedido.model_validate(pedido)
    producto.stock -= pedido.cantidad

    session.add(db_pedido)
    session.add(producto)
    session.commit()
    session.refresh(db_pedido)
    return db_pedido


@router.get("/", response_model=List[PedidoConTotal])
def listar_pedidos(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(obtener_sesion),
):
    pedidos = session.exec(select(Pedido).offset(skip).limit(limit)).all()
    resultado = []
    for p in pedidos:
        resultado.append(
            PedidoConTotal(
                id=p.id,
                cliente=p.cliente,
                cantidad=p.cantidad,
                producto_id=p.producto_id,
                fecha_pedido=p.fecha_pedido,
                total=p.cantidad * p.producto.precio,
                producto_nombre=p.producto.nombre,
            )
        )
    return resultado


@router.get("/{pedido_id}", response_model=PedidoConTotal)
def obtener_pedido(pedido_id: int, session: Session = Depends(obtener_sesion)):
    pedido = session.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return PedidoConTotal(
        id=pedido.id,
        cliente=pedido.cliente,
        cantidad=pedido.cantidad,
        producto_id=pedido.producto_id,
        fecha_pedido=pedido.fecha_pedido,
        total=pedido.cantidad * pedido.producto.precio,
        producto_nombre=pedido.producto.nombre,
    )


@router.put("/{pedido_id}", response_model=PedidoLectura)
def actualizar_pedido(
    pedido_id: int,
    datos: PedidoActualizar,
    session: Session = Depends(obtener_sesion),
):
    pedido = session.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    datos_actualizados = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(pedido, campo, valor)

    session.add(pedido)
    session.commit()
    session.refresh(pedido)
    return pedido


@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pedido(pedido_id: int, session: Session = Depends(obtener_sesion)):
    pedido = session.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    session.delete(pedido)
    session.commit()
    return None
