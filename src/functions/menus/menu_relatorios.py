from src.models.cliente import Cliente
from src.models.compra import Compra
from src.models.produto import Produto
from src.models.item_compra import ItemCompra
from sqlalchemy import func

def menu_relatorios(session):
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
            top_clientes = session.query(
                Cliente.nome,
                func.count(Compra.id_compra).label('num_compras')
            ).join(Compra).group_by(Cliente.id_cliente).order_by(
                func.count(Compra.id_compra).desc()
            ).limit(5).all()

            print("\n--- TOP 5 CLIENTES (por número de compras) ---")
            for cliente, num in top_clientes:
                print(f"{cliente}: {num} compra(s)")

        elif opcao == "2":
            top_clientes = session.query(
                Cliente.nome,
                func.sum(Compra.total_compra).label('total_gasto')
            ).join(Compra).group_by(Cliente.id_cliente).order_by(
                func.sum(Compra.total_compra).desc()
            ).limit(5).all()

            print("\n--- TOP 5 CLIENTES (por valor gasto) ---")
            for cliente, total in top_clientes:
                print(f"{cliente}: R$ {total:.2f}")

        elif opcao == "3":
            print("\n--- PRODUTOS MAIS VENDIDOS (Top 5) ---")
            top_produtos = session.query(
                Produto.nome,
                func.sum(ItemCompra.quantidade).label('qtd_vendida'),
                func.sum(ItemCompra.subtotal).label('total_vendido')
            ).join(ItemCompra, Produto.id_produto == ItemCompra.id_produto).group_by(
                Produto.id_produto
            ).order_by(
                func.sum(ItemCompra.quantidade).desc()
            ).limit(5).all()

            if not top_produtos:
                print("Nenhuma venda registrada ainda.")
            else:
                for nome, qtd, total in top_produtos:
                    total = total or 0
                    print(
                        f"{nome}: {int(qtd)} unidade(s) vendidas - R$ {total:.2f}")

        elif opcao == "4":
            total = session.query(func.sum(Compra.total_compra)).scalar() or 0
            num_compras = session.query(
                func.count(Compra.id_compra)).scalar() or 0
            print(f"\nTotal de vendas: R$ {total:.2f}")
            print(f"Número de compras: {num_compras}")

        elif opcao == "5":
            break
        else:
            print("Opção inválida!")
