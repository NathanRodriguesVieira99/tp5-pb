from src.functions.utils.assosiar_fornecedores import associar_fornecedores
from src.models.item_compra import ItemCompra
from src.models.produto import Produto


def menu_produtos(session):
    while True:
        print("\n" + "="*50)
        print("SIG - GERENCIAMENTO DE PRODUTOS")
        print("="*50)
        print("[1] Listar todos os produtos")
        print("[2] Adicionar novo produto")
        print("[3] Editar produto")
        print("[4] Deletar produto")
        print("[5] Produtos com baixo estoque")
        print("[6] Associar fornecedores")
        print("[7] Voltar")
        print("="*50)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            produtos = session.query(Produto).all()
            if not produtos:
                print("Nenhum produto cadastrado.")
            else:
                print("\n--- LISTA DE PRODUTOS ---")
                for p in produtos:
                    print(
                        f"ID: {p.id_produto} | Nome: {p.nome} | Estoque: {p.quantidade} | Preço: R$ {p.preco:.2f}")

        elif opcao == "2":
            try:
                nome = input("Nome do produto: ").strip()
                quantidade = int(input("Quantidade: "))
                preco = float(input("Preço (R$): "))

                existe = session.query(Produto).filter(
                    Produto.nome == nome).first()
                if existe:
                    print("Produto já existe!")
                else:
                    produto = Produto(
                        nome=nome, quantidade=quantidade, preco=preco)
                    session.add(produto)
                    session.commit()
                    print(f"Produto '{nome}' adicionado com sucesso!")
            except ValueError:
                print("Entrada inválida!")
                session.rollback()

        elif opcao == "3":
            try:
                id_produto = int(input("ID do produto a editar: "))
                produto = session.query(Produto).filter(
                    Produto.id_produto == id_produto).first()

                if not produto:
                    print("Produto não encontrado!")
                else:
                    print(
                        f"Produto atual: {produto.nome} | Estoque: {produto.quantidade} | Preço: R$ {produto.preco:.2f}")
                    novo_nome = input(
                        "Novo nome (ou Enter para manter): ").strip()
                    novo_estoque = input(
                        "Novo estoque (ou Enter para manter): ").strip()
                    novo_preco = input(
                        "Novo preço (ou Enter para manter): ").strip()

                    if novo_nome:
                        produto.nome = novo_nome
                    if novo_estoque:
                        produto.quantidade = int(novo_estoque)
                    if novo_preco:
                        produto.preco = float(novo_preco)

                    session.commit()
                    print("Produto atualizado com sucesso!")
            except ValueError:
                print("Entrada inválida!")
                session.rollback()

        elif opcao == "4":
            try:
                id_produto = int(input("ID do produto a deletar: "))
                produto = session.query(Produto).filter(
                    Produto.id_produto == id_produto).first()

                if not produto:
                    print("Produto não encontrado!")
                else:
                    # Verifica se existe ao menos um item de compra associado ao produto
                    existe_item = session.query(ItemCompra).filter(
                        ItemCompra.id_produto == id_produto
                    ).first()
                    if existe_item:
                        print(
                            " Não é possível deletar: existe(m) venda(s) associada(s) a este produto.")
                    else:
                        nome = produto.nome
                        session.delete(produto)
                        session.commit()
                        print(f"Produto '{nome}' deletado com sucesso!")
            except ValueError:
                print("Entrada inválida!")
                session.rollback()

        elif opcao == "5":
            limite = 10
            produtos_baixo = session.query(Produto).filter(
                Produto.quantidade < limite).all()
            if not produtos_baixo:
                print(
                    f"Nenhum produto com estoque abaixo de {limite} unidades.")
            else:
                print(f"\n--- PRODUTOS COM ESTOQUE < {limite} ---")
                for p in produtos_baixo:
                    print(
                        f"ID: {p.id_produto} | Nome: {p.nome} | Estoque: {p.quantidade}")

        elif opcao == "6":
            associar_fornecedores(session)

        elif opcao == "7":
            break
        else:
            print("Opção inválida!")
