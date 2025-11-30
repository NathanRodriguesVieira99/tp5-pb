import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


# faz o scraping e salva no CSV
def atualizar_produtos_csv(url: str, caminho: str) -> bool:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # busca  produtos
        cards = soup.find_all('div', class_='product-card')
        if not cards:
            print('Nenhum card de produto encontrado!')
            return False

        produtos = []
        for idx, card in enumerate(cards, 1):
            try:
                # extrai dados
                titulo = card.find('h5', class_='card-title')
                nome = titulo.text.strip() if titulo else f'Produto {idx}'

                # extrai preço
                preco_elem = card.find('p', class_='card-price')
                preco_text = preco_elem.get(
                    'data-preco', 'R$ 0,00') if preco_elem else 'R$ 0,00'
                preco = float(preco_text.replace(
                    'R$', '').strip().replace(',', '.'))

                # extrai quantidade/estoque
                qtd_elem = card.find('p', attrs={'data-qtd': True})
                estoque = int(qtd_elem.get('data-qtd', '0')) if qtd_elem else 0

                produtos.append({
                    'id': idx,
                    'nome': nome,
                    'estoque': estoque,
                    'preco': preco
                })
            except (ValueError, AttributeError) as e:
                continue

        if not produtos:
            print('Nenhum produto foi extraído!')
            return False

        # converte pra dataframe e salva em CSV
        df = pd.DataFrame(produtos)

        os.makedirs(os.path.dirname(caminho), exist_ok=True)

        df.to_csv(caminho, index=False, encoding='utf-8')

        print(f'{len(produtos)} produtos atualizados via scraping')
        return True

    except Exception as e:
        print(f'Erro no scraping: {e}')
        return False
