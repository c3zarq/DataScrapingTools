import requests
from bs4 import BeautifulSoup
import pandas as pd
#from pandasgui import show

# URL páginas
base_url = "https://www.auxiliadorapredial.com.br/comprar/residencial/rs+porto-alegre+centro-historico?tipoImovel=Apartamento&page="
# URL anúncios
anuncio_base_url = "https://www.auxiliadorapredial.com.br/imovel/venda/"

# Lista dados
todos_imoveis = []

# páginas de 1 a 10
for page in range(1, 11):
    url = base_url + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # localizar os blocos de anúncios na página
    for anuncio in soup.find_all('div', class_="sc-90105e55-0 fnWlcB"):
        try:
            # tipo imóvel
            tipo_completo = anuncio.find('h4').get_text()
            tipo = tipo_completo.split()[0]  # capturar primeira palavra

            # end.
            endereco = anuncio.find('span', class_="RuaSpan").get_text(strip=True)  # só a rua

            # bairro e cidade
            bairro = "centro-historico"
            cidade = "porto-alegre"
            estado = "rio-grande-do-sul"

            # Área
            area = anuncio.find('img', alt="Metragem").find_next('span').get_text(strip=True)

            # Quartos
            quartos = anuncio.find('img', alt="Quartos").find_next('span').get_text(strip=True)

            # Vagas
            vagas_tag = anuncio.find('img', alt="Garagens")
            if vagas_tag:
                vagas = vagas_tag.find_next('span').get_text(strip=True)
            else:
                vagas = '0'

            # Valor
            valor = anuncio.find('span', class_="fontSize16 bold green").get_text(strip=True)

            # cod. ref.
            codigo_ref = anuncio.find('div', class_="ref").find('span').get_text(strip=True).replace("ref:", "").strip()

            # link
            link = f"{anuncio_base_url}{codigo_ref}/{tipo}-{bairro}+{cidade}+{estado}"

            # Adicionar os dados à lista
            todos_imoveis.append({
                'Tipo': tipo,
                'Endereço': endereco,
                'Área': area,
                'Quartos': quartos,
                'Vagas': vagas,
                'Valor': valor,
                'Link': link
            })

        except AttributeError:
            print("Elemento não encontrado em algum anúncio")
            continue

# DataFrame
df_imoveis = pd.DataFrame(todos_imoveis)

# Exibir o DataFrame
print(df_imoveis)

# Se desejar visualizar o DataFrame com pandasgui
#show(df_imoveis)
