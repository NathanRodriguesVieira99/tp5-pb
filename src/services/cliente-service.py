from src.db.database import obter_sessao
from src.db.repositories.cliente_repository import ClienteRepository


class ClienteService:
    def __init__(self):
        self.session = obter_sessao()
        self.repo = ClienteRepository(self.session)

    def criar_cliente(self, nome: str):
       # valida se o nome é vazio
        if not nome or len(nome.strip()) == 0:
            raise ValueError('O nome não deve ser vazio!')

        # valida se o cliente já é cadastrado
        if self.repo.buscar_por_nome(nome):
            raise ValueError('Cliente já cadastrado!')

        return self.repo.criar(nome)

    def obter_cliente(self, id_cliente: int):
        cliente = self.repo.buscar_por_id(id_cliente)
        # valida se o cliente existe
        if not cliente:
            raise ValueError('O cliente não foi encontrado!')
        return cliente

    def listar_clientes(self):
        return self.repo.listar_todos()

    def atualizar_cliente(self, id_cliente: int, nome: str):
        # valida se o nome é vazio
        if not nome or len(nome.strip()) == 0:
            raise ValueError('O nome não deve ser vazio!')
        return self.repo.atualizar(id_cliente, nome)

    def deletar_cliente(self, id_cliente: int):
        return self.repo.deletar(id_cliente)

    def fechar(self):
        self.session.close()
