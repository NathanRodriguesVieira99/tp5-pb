from src.models.cliente import Cliente

# !! FIX -> remover contato da camada de  com banco de dados


def solicitar_id_cliente(session):
    while True:
        try:
            id_cliente = int(input('\nID do cliente (aperte 0 para sair):'))
            if id_cliente == 0:
                return None

            cliente = session.query(Cliente).filter(
                Cliente.id_cliente == id_cliente
            ).first()

            # valida se não houver cliente com o ID
            if not cliente:
                nome = input('Cliente não existe').strip()
                if nome:
                    cliente = Cliente(id_cliente=id_cliente, nome=nome)
                    session.add(cliente)
                    session.commit()
            return cliente

        except ValueError:
            print('ID inválido!')
