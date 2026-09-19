from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import crear_bd_y_tablas
from app.routers import productos, pedidos


@asynccontextmanager
async def lifespan(app: FastAPI):

    crear_bd_y_tablas()
    yield


app = FastAPI(
    title="API de Productos y Pedidos",
    description="API RESTful con FastAPI + SQLModel, desplegada en AWS EC2",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(productos.router)
app.include_router(pedidos.router)


@app.get("/", tags=["Root"])
def raiz():
    return {
        "mensaje": "API de Productos y Pedidos funcionando correctamente",
        "documentacion": "/docs",
    }
