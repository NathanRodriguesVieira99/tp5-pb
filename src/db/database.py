#  arquivo responsavel pelo db
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base


DATABASE_PATH = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), "mercado.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def obter_sessao() -> Session:
    return SessionLocal()


def iniciar_db():
    from src.models.cliente import Cliente
    from src.models.compra import Compra
    from src.models.item_compra import ItemCompra
    from src.models.produto import Produto
    from src.models.fornecedor import Fornecedor
    from src.models.produto_fornecedor import ProdutoFornecedor

    Base.metadata.create_all(engine)
    print("Banco de dados iniciado!")
