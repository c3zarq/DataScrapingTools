import requests
from bs4 import BeautifulSoup
import pandas as pd
#from pandasgui import show
import time

# extrair quant. banheiros do anúncio
def extrair_detalhes(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        banheiros_texto = soup.find('p', class_="esyJHb", string=lambda text: "banheiro" in text.lower())
        banheiros = banheiros_texto.get_text(strip=True).split()[0] if banheiros_texto else '0'
    except AttributeError:
        banheiros = '0'

    return banheiros

# dados dos anúncios
def extrair_dados(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    imoveis = []

    for anuncio in soup.find_all('a', class_="sc-613ef922-1 iJQgSL"):
        try:
            link = "https://www.creditoreal.com.br" + anuncio['href']
            tipo = anuncio.find('span', class_="imovel-type").get_text(strip=True)
            if tipo != "Apartamento":
                continue
            endereco = anuncio.find('span', class_="sc-8c367b3a-1 gOvwah").get_text(strip=True)
            area = anuncio.find_all('p', class_="esyJHb")[0].get_text(strip=True)
            quartos = anuncio.find_all('p', class_="esyJHb")[1].get_text(strip=True)
            vagas = anuncio.find_all('p', class_="esyJHb")[2].get_text(strip=True) if len(
                anuncio.find_all('p', class_="esyJHb")) > 2 else '0'
            valor = anuncio.find('p', class_="lpgNWQ").get_text(strip=True)
            banheiros = extrair_detalhes(link)

            imoveis.append({
                'Tipo': tipo,
                'Endereço': endereco,
                'Área': area,
                'Quartos': quartos,
                'Banheiros': banheiros,
                'Vagas': vagas,
                'Valor': valor,
                'Link': link
            })
            time.sleep(1)

        except AttributeError:
            print("Elemento não encontrado em algum anúncio")
            continue

    return imoveis

todos_imoveis = []
pagina = 1

while True:
    url = f"https://www.creditoreal.com.br/vendas/porto-alegre-rs/bairro/centro-historico/apartamento-residencial?filters=%7B%22valueType%22%3Atrue%2C%22cityState%22%3A%22Porto+Alegre_RS%22%2C%22neighborhoods%22%3A%5B%22Centro+Hist%C3%B3rico%22%5D%2C%22imovelTypes%22%3A%5B%22Apartamento%22%5D%7D&cityState=porto-alegre-rs&neighborhood=centro-historico&realEstateType=apartamento-residencial&page={pagina}"
    print(f"Coletando dados da página {pagina}...")

    try:
        imoveis_pagina = extrair_dados(url)
        if not imoveis_pagina:
            print("Nenhum anúncio encontrado na página, pulando para a próxima.")
            pagina += 1
            continue
        todos_imoveis.extend(imoveis_pagina)
        pagina += 1

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página {pagina}: {e}. Pulando para a próxima página.")
        pagina += 1
        continue

df = pd.DataFrame(todos_imoveis)
#show(df)
