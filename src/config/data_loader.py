import json
import csv
import os
import pandas as pd
from sqlalchemy.orm import Session
from src.models.cliente import Cliente
from src.models.produto import Produto
from src.models.fornecedor import Fornecedor
from src.models.produto_fornecedor import ProdutoFornecedor


def carregar_clientes_json(path: str, session: Session) -> int:

    # valida se o caminho o arquivo .json existe
    if not os.path.exists(path):
        print('Caminho do arquivo JSON não foi encontrado!')
        return 0

    try:
        with open(path, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        inseridos = 0
        for cliente_data in dados:
            # valida se já existe
            existe = session.query(Cliente).filter(
                Cliente.id_cliente == cliente_data['id_cliente']
            ).first()

            if not existe:
                cliente = Cliente(
                    id_cliente=cliente_data['id_cliente'],
                    nome=cliente_data['nome']
                )
                session.add(cliente)
                inseridos += 1

        session.commit()
        total = session.query(Cliente).count()
        print(f'{total} clientes carregados')
        return total

    except Exception as e:
        print(f'Erro: {e} ao carregar os clientes')
        session.rollback()
        return 0


def carregar_produtos_csv(path: str, session: Session) -> int:
    # valida se o caminho o arquivo .csv existe
    if not os.path.exists(path):
        print('Caminho do arquivo CSV não foi encontrado!')
        return 0

    try:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            inseridos = 0
            for linha in reader:
                # valida se já existe
                existe = session.query(Produto).filter(
                    Produto.nome == linha['nome'].strip()
                ).first()

                if not existe:
                    produto = Produto(
                        nome=linha['nome'].strip(),
                        quantidade=int(linha['estoque']),
                        preco=float(linha['preco'])
                    )
                    session.add(produto)
                    inseridos += 1

        session.commit()
        total = session.query(Produto).count()
        print(f'{total} produtos carregados')
        return total

    except Exception as e:
        print(f'Erro: {e} ao carregar os produtos')
        session.rollback()
        return 0


def carregar_fornecedores_excel(path: str, session: Session) -> int:
    if not os.path.exists(path):
        print('Caminho do arquivo Excel não foi encontrado!')
        return 0

    try:
        df = pd.read_excel(path, sheet_name='fornecedores')

        inseridos = 0
        for _, row in df.iterrows():
            existe = session.query(Fornecedor).filter(
                Fornecedor.nome == row['nome'].strip()
            ).first()

            if not existe:
                fornecedor = Fornecedor(nome=row['nome'].strip())
                session.add(fornecedor)
                inseridos += 1

        session.commit()
        total = session.query(Fornecedor).count()
        print(f'{total} fornecedores carregados')
        return total

    except Exception as e:
        print(f'Erro: {e} ao carregar os fornecedores')
        session.rollback()
        return 0


def carregar_produtos_fornecedores_excel(path: str, session: Session) -> int:
    if not os.path.exists(path):
        print('Caminho do arquivo Excel não foi encontrado!')
        return 0

    try:
        df = pd.read_excel(path, sheet_name='produtos-fornecedores')

        inseridos = 0
        for _, row in df.iterrows():
            existe = session.query(ProdutoFornecedor).filter(
                ProdutoFornecedor.id_produto == row['id_produto'],
                ProdutoFornecedor.id_fornecedor == row['id_fornecedor']
            ).first()

            if not existe:
                pf = ProdutoFornecedor(
                    id_produto=int(row['id_produto']),
                    id_fornecedor=int(row['id_fornecedor'])
                )
                session.add(pf)
                inseridos += 1

        session.commit()
        total = session.query(ProdutoFornecedor).count()
        print(f'{total} associações produto-fornecedor carregadas')
        return total

    except Exception as e:
        print(f'Erro: {e} ao carregar produto-fornecedor')
        session.rollback()
        return 0
