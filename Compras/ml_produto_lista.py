import requests
from bs4 import BeautifulSoup

# URL
url_base = 'https://lista.mercadolivre.com.br/'

# produto
produto = str(input('Digite o produto:\n_> '))

# busca
busca = url_base + produto

# Cabeçalhos
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# requisição
response = requests.get(busca, headers=headers)

# obj. BeautifulSoup
site = BeautifulSoup(response.text, 'html.parser')

# Encontrar produtos
produtos = site.find_all('li', attrs={'class': 'ui-search-layout__item'})

# encontrados
if not produtos:
    print("Nenhum produto encontrado. Verifique a classe CSS ou a conexão.")
else:
    for produto in produtos:
        # Título
        titulo = produto.find('a', attrs={'class': 'poly-component__title'})

        # Link
        link = titulo

        # Preço
        real = produto.find('span', attrs={'class': 'andes-money-amount__fraction'})
        cents = produto.find('span', attrs={'class': 'andes-money-amount__cents'})panela

        # info
        if titulo:
            print(titulo.text)
        else:
            print("Título não encontrado")

        if real:
            if cents:
                print(f'Preço: R$ {real.text},{cents.text}')
            else:
                print(f'Preço: R$ {real.text}')
        else:
            print("Preço não encontrado")

        if link:
            print(link['href'])
        else:
            print("Link não encontrado")

        print('\n')
