from src.sig import main as sig_main
from src.caixa import main as caixa_main
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def menu_principal():
    while True:
        print("\n" + "="*50)
        print("SUPERMERCADO - SISTEMA DE GESTÃO")
        print("="*50)
        print("[1] CAIXA - Registrar Compras")
        print("[2] SIG - Sistema de Informações Gerenciais")
        print("[0] Sair")
        print("="*50)

        try:
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                caixa_main()
            elif opcao == "2":
                sig_main()
            elif opcao == "0":
                print("\nEncerrando...")
                break
            else:
                print("Opção inválida! Tente novamente.")

        except KeyboardInterrupt:
            print("\nPrograma interrompido pelo usuário.")
            break
        except EOFError:
            print("\nEntrada encerrada.")
            break
        except Exception as e:
            print(f"Erro: {e}")
            break


if __name__ == "__main__":
    menu_principal()
