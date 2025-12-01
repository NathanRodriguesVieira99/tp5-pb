from src.db.database import iniciar_db, obter_sessao
from src.models.compra import Compra
from src.config.data_loader import carregar_clientes_json, carregar_produtos_csv
from src.config.scraper import atualizar_produtos_csv
from src.common.utils.emitir_nota_fiscal import emitir_nota_fiscal
from src.common.utils.adicionar_itens_compra import adicionar_itens_compra
from src.common.utils.solicitar_id_cliente import solicitar_id_cliente


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
