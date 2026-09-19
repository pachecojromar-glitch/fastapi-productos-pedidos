from sqlmodel import SQLModel, create_engine, Session

# SQLite para simplicidad. Si prefieres Postgres/MySQL en producción,
# cambia esta URL por la de tu motor (ej: "postgresql://usuario:pass@host/db")
DATABASE_URL = "sqlite:///./database.db"

# check_same_thread=False es necesario solo para SQLite
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def crear_bd_y_tablas():
    SQLModel.metadata.create_all(engine)


def obtener_sesion():
    with Session(engine) as session:
        yield session
