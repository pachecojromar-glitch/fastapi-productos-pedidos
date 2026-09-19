from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


# ---------------------------------------------------------------------------
# PRODUCTO
# ---------------------------------------------------------------------------
class ProductoBase(SQLModel):
    nombre: str = Field(index=True)
    descripcion: Optional[str] = None
    precio: float
    stock: int = 0


class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    pedidos: List["Pedido"] = Relationship(back_populates="producto")


class ProductoCrear(ProductoBase):
    pass


class ProductoActualizar(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None


class ProductoLectura(ProductoBase):
    id: int


# ---------------------------------------------------------------------------
# PEDIDO
# ---------------------------------------------------------------------------
class PedidoBase(SQLModel):
    cliente: str
    cantidad: int
    producto_id: int = Field(foreign_key="producto.id")
    fecha_pedido: datetime = Field(default_factory=datetime.utcnow)


class Pedido(PedidoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    producto: Optional[Producto] = Relationship(back_populates="pedidos")


class PedidoCrear(SQLModel):
    cliente: str
    cantidad: int
    producto_id: int


class PedidoActualizar(SQLModel):
    cliente: Optional[str] = None
    cantidad: Optional[int] = None
    producto_id: Optional[int] = None


class PedidoLectura(PedidoBase):
    id: int


class PedidoConTotal(PedidoLectura):
    total: float
    producto_nombre: str
