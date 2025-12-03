from src.services.relatorio_service import RelatorioService
from src.services.produto_service import ProdutoService
from src.services.cliente_service import ClienteService
from src.common.menus.menu_produtos import menu_produtos
from src.db.database import iniciar_db
from src.common.menus.menu_relatorios import menu_relatorios
from src.common.menus.menu_clientes import menu_clientes
from src.config.data_loader import carregar_fornecedores_excel, carregar_produtos_fornecedores_excel


def main():
    # inicia o db
    iniciar_db()

    # inicia os servicos
    cliente_service = ClienteService()
    produto_service = ProdutoService()
    relatorio_service = RelatorioService()

    try:
        session = produto_service.session

        # carrega o CSV e Excel
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
                menu_clientes(relatorio_service)
            elif opcao == "2":
                menu_produtos(produto_service)
            elif opcao == "3":
                menu_relatorios(relatorio_service)
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")

    except KeyboardInterrupt:
        print("\n\nSIG interrompido pelo usuário.")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
       # fecha os servicos
        cliente_service.fechar()
        produto_service.fechar()
        relatorio_service.fechar()


if __name__ == "__main__":
    main()
