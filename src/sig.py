from src.functions.menus.menu_produtos import menu_produtos
from src.db.database import obter_sessao, iniciar_db
from src.functions.menus.menu_relatorios import menu_relatorios
from src.functions.menus.menu_clientes import menu_clientes


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
