from src.services.compra_service import CompraService


def emitir_nota_fiscal(compra_service: CompraService, id_compra: int, total: float) -> None:

    try:
        compra = compra_service.obter_compra(id_compra)
    except ValueError as e:
        print(f'Erro: {e} ao emitir nota fiscal!')
        return

    cliente = compra.cliente
    itens = compra.itens

    print("\n" + "="*50)
    print("NOTA FISCAL")
    print("="*50)
    print(f"Cliente: {cliente.nome}")
    print(f"Data: {compra.data_hora.strftime('%d/%m/%Y %H:%M')}")
    print("-"*50)

    for item in itens:
        print(f"{item.produto.nome} x{item.quantidade} = R$ {item.subtotal:.2f}")

    print("-"*50)
    print(f"TOTAL: R$ {total:.2f}")
    print("="*50 + "\n")
