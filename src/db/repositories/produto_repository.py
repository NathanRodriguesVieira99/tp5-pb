from sqlalchemy.orm import Session
from src.models.produto import Produto
from src.models.item_compra import ItemCompra


class ProdutoRepository:
    def __init__(self, session: Session):
        self.session = session

    def buscar_por_id(self, id_produto: int) -> Produto:
        return self.session.query(Produto).filter(
            Produto.id_produto == id_produto
        ).first()

    def buscar_por_nome(self, nome: str) -> Produto:
        return self.session.query(Produto).filter(
            Produto.nome == nome
        ).first()

    def listar_todos(self) -> list:
        return self.session.query(Produto).all()

    # cria um novo produto
    def criar(self, nome: str, quantidade: int, preco: float) -> Produto:
        produto = Produto(nome=nome, quantidade=quantidade, preco=preco)
        self.session.add(produto)
        self.session.commit()
        return produto

    # atualiza um produto
    def atualizar(self, id_produto: int, nome: str = None, quantidade: int = None, preco: float = None) -> Produto:
        produto = self.buscar_por_id(id_produto)
        if produto:
            if nome:
                produto.nome = nome
            if quantidade:
                produto.quantidade = quantidade
            if preco:
                produto.preco = preco
            self.session.commit()
        return produto

    # deleta um produto
    def deletar(self, id_produto: int) -> bool:
        produto = self.buscar_por_id(id_produto)
        if produto:
            existe_item = self.session.query(ItemCompra).filter(
                ItemCompra.id_produto == id_produto
            ).first()
            if existe_item:
                return False

            self.session.delete(produto)
            self.session.commit()
            return True
        return False

    # busca produtos com estoque baixo
    def buscar_com_estoque_baixo(self, limite: int) -> list:
        return self.session.query(Produto).filter(
            Produto.quantidade <= limite
        ).all()

    # atualiza o estoque de produtos
    def atualizar_estoque(self, id_produto: int, quantidade: int) -> None:
        produto = self.buscar_por_id(id_produto)
        if produto:
            produto.quantidade -= quantidade
            self.session.commit()
