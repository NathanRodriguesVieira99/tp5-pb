from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import Base


class ProdutoFornecedor(Base):
    __tablename__ = "produto_fornecedor"
    
    # Colunas base
    id_produto_fornecedor: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    id_produto: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("produto.id_produto", ondelete="CASCADE"),
        nullable=False
    )
    id_fornecedor: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("fornecedor.id_fornecedor", ondelete="CASCADE"),
        nullable=False
    )
    
    def __repr__(self) -> str:
        return f"ProdutoFornecedor(produto={self.id_produto}, fornecedor={self.id_fornecedor})"
