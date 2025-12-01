from src.db.database import iniciar_db
from src.services.compra_service import CompraService
from src.services.cliente_service import ClienteService
from src.services.produto_service import ProdutoService
from src.config.data_loader import carregar_clientes_json, carregar_produtos_csv
from src.config.scraper import atualizar_produtos_csv
from src.common.utils.emitir_nota_fiscal import emitir_nota_fiscal
from src.common.utils.adicionar_itens_compra import adicionar_itens_compra
from src.common.utils.solicitar_id_cliente import solicitar_id_cliente


def main():
    print("=== ABERTURA DE CAIXA ===\n")

    # inicia o db
    iniciar_db()

    # inicia os servicos
    compra_service = CompraService()
    cliente_service = ClienteService()
    produto_service = ProdutoService()

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
        session = compra_service.session

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
                cliente = solicitar_id_cliente(cliente_service)
                if cliente:
                    compra = compra_service.criar_compra(cliente.id_cliente)

                    total = adicionar_itens_compra(
                        compra_service, produto_service, compra.id_compra)
                    if total > 0:
                        compra_service.finalizar_compra(compra.id_compra)

                        emitir_nota_fiscal(
                            compra_service, compra.id_compra, total)

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

    # fecha os servicos
    finally:
        compra_service.fechar()
        cliente_service.fechar()
        produto_service.fechar()


if __name__ == "__main__":
    main()
