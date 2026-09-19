from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import obtener_sesion
from app.models import Producto, ProductoCrear, ProductoActualizar, ProductoLectura

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/", response_model=ProductoLectura, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCrear, session: Session = Depends(obtener_sesion)):
    db_producto = Producto.model_validate(producto)
    session.add(db_producto)
    session.commit()
    session.refresh(db_producto)
    return db_producto


@router.get("/", response_model=List[ProductoLectura])
def listar_productos(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(obtener_sesion),
):
    productos = session.exec(select(Producto).offset(skip).limit(limit)).all()
    return productos


@router.get("/{producto_id}", response_model=ProductoLectura)
def obtener_producto(producto_id: int, session: Session = Depends(obtener_sesion)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.put("/{producto_id}", response_model=ProductoLectura)
def actualizar_producto(
    producto_id: int,
    datos: ProductoActualizar,
    session: Session = Depends(obtener_sesion),
):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    datos_actualizados = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(producto, campo, valor)

    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int, session: Session = Depends(obtener_sesion)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(producto)
    session.commit()
    return None
