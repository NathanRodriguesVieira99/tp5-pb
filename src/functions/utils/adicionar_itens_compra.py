from src.models.item_compra import ItemCompra
from src.models.produto import Produto

# !! FIX -> remover contato da camada de  com banco de dados


def adicionar_itens_compra(session, id_compra):
    total = 0

    while True:
        try:
            id_produto = int(input("\nID do produto (aperte 0 para sair): "))
            if id_produto == 0:
                break

            produto = session.query(Produto).filter(
                Produto.id_produto == id_produto
            ).first()

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
            subtotal = quantidade * produto.preco
            item = ItemCompra(
                id_compra=id_compra,
                id_produto=id_produto,
                quantidade=quantidade,
                preco=produto.preco,
                subtotal=subtotal
            )
            session.add(item)

            # atualiza o estoque
            produto.quantidade -= quantidade

            session.commit()
            print(f"✓ {produto.nome} x{quantidade} = R$ {subtotal:.2f}")
            total += subtotal

        except ValueError:
            print("Entrada inválida")

    return total
