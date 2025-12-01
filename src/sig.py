from src.db.database import obter_sessao, iniciar_db
from src.models.cliente import Cliente
from src.models.compra import Compra
from src.models.produto import Produto
from src.models.fornecedor import Fornecedor
from src.models.produto_fornecedor import ProdutoFornecedor
from src.models.item_compra import ItemCompra
from sqlalchemy import func


def menu_clientes(session):
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
            clientes_com_compras = session.query(
                Cliente).join(Compra).distinct().all()
            if not clientes_com_compras:
                print("Nenhum cliente com compras encontrado!")
            else:
                print("\n--- CLIENTES COM COMPRAS ---")
                for cliente in clientes_com_compras:
                    total_gasto = session.query(func.sum(Compra.total_compra)).filter(
                        Compra.id_cliente == cliente.id_cliente
                    ).scalar() or 0
                    print(
                        f"ID: {cliente.id_cliente} | Nome: {cliente.nome} | Total Gasto: R$ {total_gasto:.2f}")

        elif opcao == "2":
            clientes_sem_compras = session.query(Cliente).outerjoin(Compra).filter(
                Compra.id_compra == None
            ).all()
            if not clientes_sem_compras:
                print("Todos os clientes têm compras.")
            else:
                print("\n--- CLIENTES SEM COMPRAS ---")
                for cliente in clientes_sem_compras:
                    print(f"ID: {cliente.id_cliente} | Nome: {cliente.nome}")

        elif opcao == "3":
            break
        else:
            print("❌ Opção inválida!")


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


def associar_fornecedores(session):
    try:
        id_produto = int(input("ID do produto: "))
        produto = session.query(Produto).filter(
            Produto.id_produto == id_produto).first()

        if not produto:
            print("Produto não encontrado!")
            return

        fornecedores = session.query(Fornecedor).all()
        if not fornecedores:
            print("Nenhum fornecedor cadastrado!")
            return

        print(f"\nProduto: {produto.nome}")
        print("\n--- FORNECEDORES DISPONÍVEIS ---")
        for f in fornecedores:
            print(f"ID: {f.id_fornecedor} | Nome: {f.nome}")

        id_fornecedor = int(input("\nID do fornecedor: "))
        fornecedor = session.query(Fornecedor).filter(
            Fornecedor.id_fornecedor == id_fornecedor).first()

        if not fornecedor:
            print("Fornecedor não encontrado!")
            return

        existe = session.query(ProdutoFornecedor).filter(
            ProdutoFornecedor.id_produto == id_produto,
            ProdutoFornecedor.id_fornecedor == id_fornecedor
        ).first()

        if existe:
            print("Esta associação já existe!")
        else:
            pf = ProdutoFornecedor(id_produto=id_produto,
                                   id_fornecedor=id_fornecedor)
            session.add(pf)
            session.commit()
            print(
                f"✓ Fornecedor '{fornecedor.nome}' associado ao produto '{produto.nome}'!")

    except ValueError:
        print("Entrada inválida!")
        session.rollback()


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


def main():
    iniciar_db()
    session = obter_sessao()

    try:
        from src.config.data_loader import carregar_fornecedores_excel, carregar_produtos_fornecedores_excel

        print("Carregando dados do SIG...")
        carregar_fornecedores_excel(
            "src/config/excel/fornecedores.xlsx", session)
        carregar_produtos_fornecedores_excel(
            "src/config/excel/fornecedores.xlsx", session)
        print()

        while True:
            print("\n" + "="*50)
            print("SISTEMA DE INFORMAÇÕES GERENCIAIS - SIG")
            print("="*50)
            print("[1] Gerenciamento de Clientes")
            print("[2] Gerenciamento de Produtos")
            print("[3] Relatórios")
            print("[0] Voltar")
            print("="*50)

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                menu_clientes(session)
            elif opcao == "2":
                menu_produtos(session)
            elif opcao == "3":
                menu_relatorios(session)
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")

    except KeyboardInterrupt:
        print("\n\nSIG interrompido pelo usuário.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
