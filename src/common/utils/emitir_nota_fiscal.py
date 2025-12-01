from src.models.item_compra import ItemCompra
from src.models.produto import Produto

# !! FIX -> remover contato da camada de  com banco de dados


def emitir_nota_fiscal(session, cliente, compra, total):
    print("\n" + "="*50)
    print("NOTA FISCAL")
    print("="*50)
    print(f"Cliente: {cliente.nome}")
    print(f"Data: {compra.data_hora.strftime('%d/%m/%Y %H:%M')}")
    print("-"*50)

    itens = session.query(ItemCompra).filter(
        ItemCompra.id_compra == compra.id_compra
    ).all()

    for item in itens:
        produto = session.query(Produto).filter(
            Produto.id_produto == item.id_produto
        ).first()
        print(f"{produto.nome} x{item.quantidade} = R$ {item.subtotal:.2f}")

    print("-"*50)
    print(f"TOTAL: R$ {total:.2f}")
    print("="*50 + "\n")

    # atualizar total  compra
    compra.total_compra = total
    session.commit()
