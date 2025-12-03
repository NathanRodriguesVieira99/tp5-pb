from src.services.relatorio_service import RelatorioService
from src.models.item_compra import ItemCompra
from src.models.compra import Compra


def menu_relatorios(relatorio_service: RelatorioService):
    while True:
        print("\n" + "="*50)
        print("SIG - RELATÓRIOS")
        print("="*50)
        print("[1] Top 5 clientes por número de compras")
        print("[2] Top 5 clientes por valor gasto")
        print("[3] Produtos mais vendidos")
        print("[4] Total de vendas")
        print("[5] Voltar")
        print("="*50)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            top_clientes = relatorio_service.top_clientes_por_compras(5)
            for cliente, num_compras in top_clientes:
                print(f'{cliente.nome}: {num_compras} compra(s)')
            print("\n--- TOP 5 CLIENTES (por número de compras) ---")
            for cliente, num in top_clientes:
                print(f"{cliente}: {num} compra(s)")

        elif opcao == "2":
            top_clientes = relatorio_service.top_clientes_por_gasto(5)
            for cliente, valor_total in top_clientes:
                print(f'{cliente.nome}: R$ {valor_total:.2f}')

            print("\n--- TOP 5 CLIENTES (por valor gasto) ---")
            for cliente, total in top_clientes:
                print(f"{cliente}: R$ {total:.2f}")

        elif opcao == "3":
            print("\n--- PRODUTOS MAIS VENDIDOS (Top 5) ---")
            top_produtos = relatorio_service.produtos_mais_vendidos(5)
            for produto, qtd_vendida in top_produtos:
                total_vendido = produto.preco * qtd_vendida
                print(
                    f'{produto.nome}: {int(qtd_vendida)} unidades - R$ {total_vendido:.2f}')

            if not top_produtos:
                print("Nenhuma venda registrada ainda.")
            else:
                for nome, qtd, total in top_produtos:
                    total = total or 0
                    print(
                        f"{nome}: {int(qtd)} unidade(s) vendidas - R$ {total:.2f}")

        elif opcao == "4":
            #  usa session instanciada no service ao invés de session direta (via ORM)
            total = relatorio_service.session.query(
                __import__('sqlalchemy', fromlist=['func']).func.sum(
                    ItemCompra.subtotal)
            ).scalar() or 0
            num_compras = relatorio_service.session.query(
                __import__('sqlalchemy', fromlist=[
                           'func']).func.count(Compra.id_compra)
            ).scalar() or 0

            print(f"\nTotal de vendas: R$ {total:.2f}")
            print(f"Número de compras: {num_compras}")

        elif opcao == "5":
            break
        else:
            print("Opção inválida!")
