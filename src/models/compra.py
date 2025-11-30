from datetime import datetime
from sqlalchemy import Integer, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base


class Compra(Base):
    __tablename__ = "compra"

    # Colunas base
    id_compra: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    id_cliente: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cliente.id_cliente", ondelete="CASCADE"),
        nullable=False
    )
    data_hora: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    total_compra: Mapped[float] = mapped_column(
        Numeric(10, 2, asdecimal=False),
        default=0.00
    )

    # Relacionamentos
    cliente = relationship(
        "Cliente",
        back_populates="compras"
    )
    itens = relationship(
        "ItemCompra",
        back_populates="compra",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Compra(id={self.id_compra}, cliente={self.id_cliente}, total={self.total_compra})"

    def __str__(self) -> str:
        return f"Compra #{self.id_compra} - {self.data_hora.strftime('%d/%m/%Y %H:%M')} - R$ {self.total_compra:.2f}"

    def calcular_total(self) -> float:
        return sum(item.subtotal for item in self.itens)

    def atualizar_total(self) -> None:
        self.total_compra = self.calcular_total()
