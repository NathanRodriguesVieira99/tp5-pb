from sqlalchemy import func
from src.models.cliente import Cliente
from src.models.compra import Compra


def menu_clientes(session):
    while True:
        print("\n" + "="*50)
        print("SIG - GERENCIAMENTO DE CLIENTES")
        print("="*50)
        print("[1] Listar clientes com compras")
        print("[2] Listar clientes sem compras")
        print("[3] Voltar")
        print("="*50)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            clientes_com_compras = session.query(
                Cliente).join(Compra).distinct().all()
            if not clientes_com_compras:
                print("Nenhum cliente com compras encontrado!")
            else:
                print("\n--- CLIENTES COM COMPRAS ---")
                for cliente in clientes_com_compras:
                    total_gasto = session.query(func.sum(Compra.total_compra)).filter(
                        Compra.id_cliente == cliente.id_cliente
                    ).scalar() or 0
                    print(
                        f"ID: {cliente.id_cliente} | Nome: {cliente.nome} | Total Gasto: R$ {total_gasto:.2f}")

        elif opcao == "2":
            clientes_sem_compras = session.query(Cliente).outerjoin(Compra).filter(
                Compra.id_compra == None
            ).all()
            if not clientes_sem_compras:
                print("Todos os clientes têm compras.")
            else:
                print("\n--- CLIENTES SEM COMPRAS ---")
                for cliente in clientes_sem_compras:
                    print(f"ID: {cliente.id_cliente} | Nome: {cliente.nome}")

        elif opcao == "3":
            break
        else:
            print("Opção inválida!")
