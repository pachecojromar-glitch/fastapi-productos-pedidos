from sqlmodel import SQLModel, create_engine, Session


DATABASE_URL = "sqlite:///./database.db"


engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def crear_bd_y_tablas():
    SQLModel.metadata.create_all(engine)


def obtener_sesion():
    with Session(engine) as session:
        yield session
