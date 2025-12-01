from typing import Optional
from src.models.cliente import Cliente
from src.services.cliente_service import ClienteService


def solicitar_id_cliente(cliente_service: ClienteService) -> Optional[Cliente]:
    while True:
        try:
            id_cliente = int(input('\nID do cliente (aperte 0 para sair):'))
            if id_cliente == 0:
                return None

            try:
                cliente = cliente_service.obter_cliente(id_cliente)
                return cliente
            except ValueError:
                print("Cliente não encontrado.")

        except ValueError:
            print('ID inválido!')
