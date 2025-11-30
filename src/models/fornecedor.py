from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base


class Fornecedor(Base):

    __tablename__ = "fornecedor"

   # Colunas base
    id_fornecedor: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

   # Relacionamentos
    produtos = relationship(
        "Produto",
        secondary="produto_fornecedor",
        back_populates="fornecedores"
    )

    def __repr__(self) -> str:
        return f"Fornecedor(id={self.id_fornecedor}, nome={self.nome})"

    def __str__(self) -> str:
        return f"[{self.id_fornecedor:03d}] {self.nome}"
