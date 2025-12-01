from src.services.produto_service import ProdutoService
from src.services.compra_service import CompraService


def adicionar_itens_compra(compra_service: CompraService,
                           produto_service: ProdutoService, id_compra: int) -> float:
    total = 0

    while True:
        try:
            id_produto = int(
                input("\nID do produto (aperte 0 para sair): "))
            if id_produto == 0:
                break

            produto = produto_service.obter_produto(id_produto)

            # valida se o produto não existe
            if not produto:
                print("O Produto não foi encontrado!")
                continue

            # valida se o produto tem estoque menor que 0
            quantidade = int(input("Quantidade: "))
            if quantidade <= 0:
                print("Quantidade inválida")
                continue

            # valida se o produto tem estoque
            if quantidade > produto.quantidade:
                print(
                    f"Estoque insuficiente. Estoque disponível: {produto.quantidade}")
                continue

            # criar um item
            try:
                item = compra_service.adicionar_item_compra(
                    id_compra, id_produto, quantidade)
                print("\n" + "="*50)
                print(
                    f'Produto: {produto.nome} x{quantidade} = R$ {item.subtotal:.2f}')
                total += item.subtotal
            except ValueError as e:
                print(f'Erro: {e}')

        except ValueError:
            print("Entrada inválida")

    return total
