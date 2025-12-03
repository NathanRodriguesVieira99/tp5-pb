from src.services.produto_service import ProdutoService


def associar_fornecedores(produto_service: ProdutoService):
    try:
        id_produto = int(input("ID do produto: "))
        
        # usa service para obter produto
        try:
            produto = produto_service.obter_produto(id_produto)
        except ValueError as e:
            print(f"Erro: {e}")
            return

        Fornecedor = __import__('src.models.fornecedor', fromlist=['Fornecedor']).Fornecedor
        fornecedores = produto_service.repo.session.query(Fornecedor).all()
        
        if not fornecedores:
            print("Nenhum fornecedor cadastrado!")
            return

        print(f"\nProduto: {produto.nome}")
        print("\n--- FORNECEDORES DISPONÍVEIS ---")
        for f in fornecedores:
            print(f"ID: {f.id_fornecedor} | Nome: {f.nome}")

        id_fornecedor = int(input("\nID do fornecedor: "))
        
        # busca fornecedor via session do service
        fornecedor = produto_service.repo.session.query(Fornecedor).filter(
            Fornecedor.id_fornecedor == id_fornecedor
        ).first()

        if not fornecedor:
            print("Fornecedor não encontrado!")
            return


        if fornecedor in produto.fornecedores:
            print("Esta associação já existe!")
        else:
            produto.fornecedores.append(fornecedor)
            produto_service.repo.session.commit()
            print(f"✓ Fornecedor '{fornecedor.nome}' associado ao produto '{produto.nome}'!")

    except ValueError:
        print("Entrada inválida!")
        produto_service.repo.session.rollback()
    except Exception as e:
        print(f"Erro: {e}")
        produto_service.repo.session.rollback()
