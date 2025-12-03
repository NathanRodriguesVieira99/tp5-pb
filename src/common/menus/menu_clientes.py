from src.services.relatorio_service import RelatorioService


def menu_clientes(relatorio_service: RelatorioService):
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
            clientes_com_compras = relatorio_service.clientes_com_compras()
            if not clientes_com_compras:
                print("Nenhum cliente com compras encontrado!")

            else:
                print("\n--- CLIENTES COM COMPRAS ---")
                for cliente in clientes_com_compras:

                    total_gasto = sum(
                        sum(item.subtotal for item in compra.itens)
                        for compra in cliente.compras
                    )
                    print(
                        f"ID: {cliente.id_cliente} | Nome: {cliente.nome} | Total Gasto: R$ {total_gasto:.2f}")

        elif opcao == "2":
            clientes_sem_compras = relatorio_service.clientes_sem_compra()
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
