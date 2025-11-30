from sqlalchemy.orm import Session
from src.models.cliente import Cliente


class ClienteRepository:
    def __init__(self, session: Session):
        self.session = session

    def buscar_por_id(self, id_cliente: int) -> Cliente:
        return self.session.query(Cliente).filter(
            Cliente.id_cliente == id_cliente
        ).first()

    def buscar_por_nome(self, nome: str) -> Cliente:
        return self.session.query(Cliente).filter(
            Cliente.nome == nome
        ).first()

    def listar_todos(self) -> list:
        return self.session.query(Cliente).all()

    # cria um novo cliente
    def criar(self, nome: str) -> Cliente:
        cliente = Cliente(nome=nome)
        self.session.add(cliente)
        self.session.commit()
        return cliente

    # atualizar o cliente
    def atualizar(self, id_cliente: int, nome: str) -> Cliente:
        cliente = self.buscar_por_id(id_cliente)
        if cliente:
            cliente.nome = nome
            self.session.commit()
        return cliente

    # deletar o cliente
    def deletar(self, id_cliente: int) -> bool:
        cliente = self.buscar_por_id(id_cliente)
        if cliente:
            self.session.delete(cliente)
            self.session.commit()
            return True
        return False
