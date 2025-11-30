from src.db.database import iniciar_db, obter_sessao
from src.models.cliente import Cliente
from src.models.compra import Compra
from src.models.item_compra import ItemCompra
from src.models.produto import Produto
from src.config.data_loader import carregar_clientes_json, carregar_produtos_csv
from src.config.scraper import atualizar_produtos_csv


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


def main():
    print("=== ABERTURA DE CAIXA ===\n")

    # inicia o db
    iniciar_db()
    session = obter_sessao()

    try:
        # faz scraping dos produtos
        print("Atualizando produtos via web scraping...")
        PRODUTOS_URL = "https://pedrovncs.github.io/lindosprecos/produtos.html"
        PRODUTOS_CSV = "src/config/csv/produtos.csv"

        if not atualizar_produtos_csv(PRODUTOS_URL, PRODUTOS_CSV):
            print("Scraping falhou!\n")
        else:
            print()

        # carrega dados
        print("Carregando clientes...")
        carregar_clientes_json("src/config/json/clientes.json", session)

        print("Carregando produtos...")
        carregar_produtos_csv(PRODUTOS_CSV, session)
        print()

        # vendas
        totais = []

        while True:
            print("\n[i] Iniciar venda  [f] Fechar caixa")
            opcao = input("Opção: ").strip().lower()

            if opcao == 'f':
                break
            elif opcao == 'i':
                cliente = solicitar_id_cliente(session)
                if cliente:
                    compra = Compra(id_cliente=cliente.id_cliente)
                    session.add(compra)
                    session.commit()

                    total = adicionar_itens_compra(session, compra.id_compra)
                    if total > 0:
                        emitir_nota_fiscal(session, cliente, compra, total)
                        totais.append(total)

        # fecha o caixa
        print("\n" + "="*50)
        print("FECHAMENTO DE CAIXA")
        print("="*50)
        print(f"Número de vendas: {len(totais)}")
        if totais:
            print(f"Total do dia: R$ {sum(totais):.2f}")
        else:
            print("Nenhuma venda realizada")
        print("="*50)

    finally:
        session.close()


if __name__ == "__main__":
    main()
