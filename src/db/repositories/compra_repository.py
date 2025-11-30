from sqlalchemy.orm import Session
from src.models.compra import Compra
from sqlalchemy import desc
from src.models.item_compra import ItemCompra


class CompraRepository:
    def __init__(self, session: Session):
        self.session = session

    def buscar_por_id(self, id_compra: int) -> Compra:
        return self.session.query(Compra).filter(
            Compra.id_compra == id_compra
        ).first()

    def buscar_por_cliente(self, id_cliente: int) -> list:
        return self.session.query(Compra).filter(
            Compra.id_cliente == id_cliente
        ).order_by(desc(Compra.data_hora)).all()

    def criar_compra(self, id_cliente: int) -> Compra:
        compra = Compra(id_cliente=id_cliente)
        self.session.add(compra)
        self.session.commit()
        return compra

    def adicionar_item(self, id_compra: int, id_produto: int,
                       quantidade: int, preco: float) -> ItemCompra:
        subtotal = quantidade * preco
        item = ItemCompra(
            id_compra=id_compra,
            id_produto=id_produto,
            quantidade=quantidade,
            preco=preco,
            subtotal=subtotal
        )
        self.session.add(item)
        self.session.commit()
        return item

    def finalizar_compra(self, id_compra: int) -> Compra:
        compra = self.buscar_por_id(id_compra)
        if compra:
            compra.atualizar_total()  # utiliza a funcao antes de finalizar
            self.session.commit()
        return compra

    def listar_todas(self) -> list:
        return self.session.query(Compra).order_by(desc(Compra.data_hora)).all()
