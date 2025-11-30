from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base


class Cliente(Base):
    __tablename__ = "cliente"

# Colunas Base
    id_cliente: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )
    data_cadastro: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

# Relacionamentos
    compras = relationship(
        "Compra",
        back_populates="cliente",
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Cliente(id{self.id_cliente}, nome={self.nome})"

    def __str__(self):
        return f"[{self.id_cliente: 03d}] {self.nome}"
