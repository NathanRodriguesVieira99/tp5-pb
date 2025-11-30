from src.db.database import obter_sessao
from src.db.repositories.produto_repository import ProdutoRepository


class ProdutoService:
    def __init__(self):
        self.session = obter_sessao()
        self.repo = ProdutoRepository(self.session)

    def criar_produto(self, nome: str, quantidade: int, preco: float):
        # valida se o nome do produto é vazio
        if not nome or len(nome.strip()) == 0:
            raise ValueError('O nome não deve ser vazio!')

        # valida se o preco é maior que 0
        if preco <= 0:
            raise ValueError('O preco deve ser maior que 0!')

        # valida se a quantidade é maior que 0
        if quantidade < 0:
            raise ValueError('A quantidade deve ser maior que 0!')

        # valida se o produto ja existe
        if self.repo.buscar_por_nome(nome):
            raise ValueError(f'O produto: "{nome}" já está cadastrado!')

        return self.repo.criar(nome, quantidade, preco)

    def obter_produto(self, id_produto: int):
        produto = self.repo.buscar_por_id(id_produto)

        # valida se o produto existe
        if not produto:
            raise ValueError(f'O produto: "{id_produto}" não existe!')

        return produto

    def listar_produtos(self):
        return self.repo.listar_todos()

    def atualizar_produto(self, id_produto: int, nome: str, quantidade: int, preco: float):

        # valida se o preco é maior que 0
        if preco <= 0:
            raise ValueError('O preco deve ser maior que 0!')

         # valida se a quantidade é maior que 0
        if quantidade < 0:
            raise ValueError('A quantidade deve ser maior que 0!')

        return self.repo.atualizar(id_produto, nome, quantidade, preco)

    def deletar_produto(self, id_produto: int):
        return self.deletar_produto(id_produto)

    def produtos_com_baixo_estoque(self, limite: int) -> list:
        return self.repo.buscar_com_estoque_baixo(limite)

    def atualizar_estoque(self, id_produto: int, quantidade: int):
        self.repo.atualizar_estoque(id_produto, quantidade)

    def fechar(self):
        self.session.close()
