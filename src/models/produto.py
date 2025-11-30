from datetime import datetime
from sqlalchemy import Integer, String, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base


class Produto(Base):
    __tablename__ = "produto"

   # Colunas Base
    id_produto: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )
    quantidade: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    preco: Mapped[float] = mapped_column(
        Numeric(10, 2, asdecimal=False),
        nullable=False
    )
    data_atualizacao: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )

    # Relacionamentos
    itens_compra = relationship(
        "ItemCompra",
        back_populates="produto",
        cascade="all, delete-orphan"
    )
    fornecedores = relationship(
        "Fornecedor",
        secondary="produto_fornecedor",
        back_populates="produtos"
    )

    def __repr__(self) -> str:
        return f"Produto(id={self.id_produto}, nome={self.nome}, estoque={self.quantidade})"

    def __str__(self) -> str:
        return f"[{self.id_produto:03d}] {self.nome} - Qtd: {self.quantidade} | R$ {self.preco:.2f}"

    def tem_estoque_disponivel(self, quantidade: int) -> bool:
        return quantidade <= self.quantidade

    def em_baixo_estoque(self, limite: int) -> bool:
        return self.quantidade <= limite
