from sqlalchemy.orm import Session
from src.models.fornecedor import Fornecedor
from src.models.produto import Produto


class FornecedorRepository:
    def __init__(self, session: Session):
        self.session = session

        def buscar_por_id(self, id_fornecedor: int) -> Fornecedor:
            return self.session.query(Fornecedor).filter(
                Fornecedor.id_fornecedor == id_fornecedor
            ).first()

        def buscar_por_nome(self, nome: str) -> Fornecedor:
            return self.session.query(Fornecedor).filter(
                Fornecedor.nome == nome
            ).first()

        def listar_todos(self) -> list:
            return self.session.query(Fornecedor).all()

        def criar(self, nome: str) -> Fornecedor:
            fornecedor = Fornecedor(nome=nome)
            self.session.add(Fornecedor)
            self.session.commit()
            return fornecedor

        def atualizar(self, id_fornecedor: int, nome: str) -> Fornecedor:
            fornecedor = self.buscar_por_id(id_fornecedor)
            if fornecedor:
                fornecedor.nome = nome
            self.session.commit()
            return fornecedor

        def deletar(self, id_fornecedor: int) -> bool:
            fornecedor = self.buscar_por_id(id_fornecedor)
            if fornecedor:
                self.session.delete(fornecedor)
                self.session.commit()
                return True
            return False

        def buscar_fornecedores_por_produto(self, id_produto: int) -> list:
            produto = self.session.query(Produto).filter(
                Produto.id_produto == id_produto
            ).first()
            if produto:
                return produto.fornecedores
            return []
