from sqlalchemy import func, desc
from src.db.database import obter_sessao
from src.models.cliente import Cliente
from src.models.compra import Compra
from src.models.item_compra import ItemCompra
from src.models.produto import Produto


class RelatorioService:
    def __init__(self):
        self.session = obter_sessao()

    def clientes_com_compras(self) -> list:
        return self.session.query(Cliente).join(Compra).distinct().all()

    def clientes_sem_compra(self) -> list:
        return self.session.query(Cliente).outerjoin(Compra).filter(
            Compra.id_compra.is_(None)
        ).all()

    def top_clientes_por_compras(self, limite: int = 5) -> list:
        return self.session.query(
            Cliente,
            func.count(Compra.id_compra).label('total_compras')
        ).join(Compra).group_by(Cliente.id_cliente).order_by(
            desc('total_compras')
        ).limit(limite).all()

    def top_clientes_por_gasto(self, limite: int = 5) -> list:
        return self.session.query(
            Cliente,
            func.sum(Compra.total_compra).label('valor_total')
        ).join(Compra).group_by(Cliente.id_cliente).order_by(
            desc('valor_total')
        ).limit(limite).all()

    def produtos_mais_vendidos(self, limite: int = 5) -> list:
        return self.session.query(
            Produto,
            func.sum(ItemCompra.quantidade).label('total_vendido')
        ).join(ItemCompra).group_by(Produto.id_produto).order_by(
            desc('total_vendido')
        ).limit(limite).all()

    def produtos_menos_vendidos(self, limite: int = 5) -> list:
        return self.session.query(
            Produto,
            func.coalesce(func.sum(ItemCompra.quantidade),
                          0).label('total_vendido')
        ).outerjoin(ItemCompra).group_by(Produto.id_produto).order_by(
            desc('total_vendido')
        ).limit(limite).all()

    def produtos_com_baixo_estoque(self, limite: int):
        return self.session.query(Produto).filter(
            Produto.quantidade <= limite
        ).all()

    def fornecedores_por_produto(self, id_produto: int):
        produto = self.session.query(Produto).filter(
            Produto.id_produto == id_produto
        ).first()
        if produto:
            return produto.fornecedores
        return []

    def fechar(self):
        self.session.close()
