from src.db.database import obter_sessao
from src.db.repositories.produto_repository import ProdutoRepository
from src.db.repositories.compra_repository import CompraRepository


class CompraService:
    def __init__(self):
        self.session = obter_sessao()
        self.repo_compra = CompraRepository(self.session)
        self.repo_produto = ProdutoRepository(self.session)

    def criar_compra(self, id_cliente: int):
        return self.repo_compra.criar_compra(id_cliente)

    def adicionar_item_compra(self, id_compra: int, id_produto: int, quantidade: int):
        produto = self.repo_produto.buscar_por_id(id_produto)

        # verifica se o produto existe
        if not produto:
            raise ValueError('O produto não existe!')

        # verifica se o produto está em estoque
        if not produto.tem_estoque_disponivel(quantidade):
            raise ValueError(
                f'Produto com estoque insuficiente! Estoque disponivel: {produto.quantidade}')

        # adiciona item a compra
        item = self.repo_compra.adicionar_item(
            id_compra, id_produto, quantidade, produto.preco)

        # atualiza o estoque após a compra
        self.repo_produto.atualizar_estoque(id_produto, quantidade)
        return item

    def finalizar_compra(self, id_compra: int):
        compra = self.repo_compra.buscar_por_id(id_compra)

        # valida se a compra existe
        if not compra:
            raise ValueError(f'A compra: "{id_compra}" não existe!')
        return compra

    def obter_compra(self, id_compra: int):
        compra = self.repo_compra.buscar_por_id(id_compra)

        # valida se a compra existe
        if not compra:
            raise ValueError(f'A compra: "{id_compra}" não existe!')
        return compra

    def listar_compras_cliente(self, id_cliente: int):
        return self.repo_compra.buscar_por_cliente(id_cliente)

    def fechar(self):
        self.session.close()
