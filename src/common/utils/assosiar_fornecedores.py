from src.models.fornecedor import Fornecedor
from src.models.produto import Produto
from src.models.produto_fornecedor import ProdutoFornecedor

# !! FIX -> remover contato da camada de  com banco de dados


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
