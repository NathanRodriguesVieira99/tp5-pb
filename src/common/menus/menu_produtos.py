from src.services.produto_service import ProdutoService
from src.common.utils.associar_fornecedores import associar_fornecedores


def menu_produtos(produto_service: ProdutoService):
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
            produtos = produto_service.listar_produtos()

            if not produtos:
                print("Nenhum produto cadastrado.")

            else:
                print("\n--- LISTA DE PRODUTOS ---")
                for p in produtos:
                    print(
                        f"ID: {p.id_produto} | Nome: {p.nome} | Estoque: {p.quantidade} | Preço: R$ {p.preco:.2f}")

        elif opcao == "2":
            try:
               # usuario informa os valores (nome, quantidade e preco)
                nome = input("Nome do produto: ").strip()
                quantidade = int(input("Quantidade: "))
                preco = float(input("Preço (R$): "))

                produto = produto_service.criar_produto(
                    nome, quantidade, preco)
                print(f"Produto '{nome}' adicionado com sucesso!")

            except ValueError as e:
                print(f'Erro: {e}')

        elif opcao == "3":
            try:
                id_produto = int(input("ID do produto a editar: "))

              # obtem o ID do produto que vai ser editado
                produto = produto_service.obter_produto(id_produto)

              # exibe dados atuais do produto
                print(
                    f"Produto atual: {produto.nome} | Estoque: {produto.quantidade} | Preço: R$ {produto.preco:.2f}")

                # usuario informa o novo nome
                novo_nome = input("Novo nome (ou Enter para manter): ").strip()

                # usuario informa o novo estoque
                novo_estoque = input(
                    "Novo estoque (ou Enter para manter): ").strip()

                # usuario informa o novo preco
                novo_preco = input(
                    "Novo preço (ou Enter para manter): ").strip()

                nome_final = novo_nome if novo_nome else produto.nome

                estoque_final = int(
                    novo_estoque) if novo_estoque else produto.quantidade

                preco_final = float(
                    novo_preco) if novo_preco else produto.preco

                produto_service.atualizar_produto(
                    id_produto, nome_final, estoque_final, preco_final)
                print("Produto atualizado com sucesso!")

            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "4":
            try:
                id_produto = int(input("ID do produto a deletar: "))

                # obtem o ID do produto a ser deletado
                produto = produto_service.obter_produto(id_produto)

               # deleta o produto pelo ID
                produto_service.deletar_produto(id_produto)
                print(f"Produto '{produto.nome}' deletado com sucesso!")

            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "5":
            limite = 10  # limite de estoque

            produtos_baixo_estoque = produto_service.produtos_com_baixo_estoque(
                limite)

            if not produtos_baixo_estoque:
                print(
                    f"Nenhum produto com estoque abaixo de {limite} unidades.")

            else:
                # produtos com estoque < 10
                print(f"\n--- PRODUTOS COM ESTOQUE < {limite} ---")
                for p in produtos_baixo_estoque:
                    print(
                        f"ID: {p.id_produto} | Nome: {p.nome} | Estoque: {p.quantidade}")

        elif opcao == "6":
            associar_fornecedores(produto_service)

        elif opcao == "7":
            break
        else:
            print("Opção inválida!")
