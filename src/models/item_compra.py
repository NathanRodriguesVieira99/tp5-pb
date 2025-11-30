from sqlalchemy import Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base


class ItemCompra(Base):  
    __tablename__ = "item_compra"
    
    # Colunas base
    id_item: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    id_compra: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("compra.id_compra", ondelete="CASCADE"),
        nullable=False
    )
    id_produto: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("produto.id_produto", ondelete="RESTRICT"),
        nullable=False
    )
    quantidade: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    preco: Mapped[float] = mapped_column(
        Numeric(10, 2, asdecimal=False),
        nullable=False
    )
    subtotal: Mapped[float] = mapped_column(
        Numeric(10, 2, asdecimal=False),
        nullable=False
    )
    
    # Relacionamentos
    compra = relationship(
        "Compra",
        back_populates="itens"
    )
    produto = relationship(
        "Produto",
        back_populates="itens_compra"
    )
    
    def __repr__(self) -> str:
        return f"ItemCompra(compra={self.id_compra}, produto={self.id_produto}, qty={self.quantidade})"
    
    def __str__(self) -> str:
        nome_produto = self.produto.nome if self.produto else "Desconhecido"
        return f"{nome_produto} x{self.quantidade} @ R$ {self.preco:.2f} = R$ {self.subtotal:.2f}"
