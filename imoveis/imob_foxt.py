import requests
from bs4 import BeautifulSoup
import pandas as pd
#from pandasgui import show

# URL base anúncios
base_url = "https://www.foxterciaimobiliaria.com.br/imoveis/a-venda/em-porto-alegre-rs/apartamento/no-bairro-centro-historico?page="

# lista dados
todos_imoveis = []

# páginas de 1 a 10
for page in range(1, 11):
    url = base_url + str(page)
    print(f"Processando página {page}...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # localizar blocos anúncios
    anuncios = soup.find_all('section',
                             class_="flex-col px-4 md:-mx-2 pt-1 pb-2 mb-4 hover:bg-slate-100 rounded-2xl transition-colors duration-500")
    if anuncios:
        print(f"Encontrou {len(anuncios)} anúncios na página {page}.")
    else:
        print(f"Nenhum anúncio encontrado na página {page}.")

    for anuncio in anuncios:
        try:
            # tipo
            tipo_completo_tag = anuncio.find('div',
                                             class_="flex text-sm justify-start text-foxter-brand-900 font-bold mb-2")
            if tipo_completo_tag:
                tipo_completo = tipo_completo_tag.get_text(strip=True)
                tipo = tipo_completo.split(" ")[0]
                print(f"Tipo encontrado: {tipo}")

                # End.
                endereco_tag = tipo_completo_tag.find_next('div')
                if endereco_tag:
                    endereco_completo = endereco_tag.get_text(strip=True)
                    endereco = endereco_completo.split(",")[0]
                    print(f"Endereço encontrado: {endereco}")
                else:
                    print("Endereço não encontrado.")
                    endereco = "N/A"
            else:
                print("Tipo não encontrado.")
                tipo, endereco = "N/A", "N/A"

            # Área
            area_tag = anuncio.find('span', class_="whitespace-nowrap text-foxter-brand-900")
            if area_tag:
                area = area_tag.find('strong').get_text(strip=True)
                print(f"Área encontrada: {area} m²")
            else:
                print("Área não encontrada.")
                area = "N/A"

            # Quartos
            quartos_tag = anuncio.find_all('span', class_="whitespace-nowrap text-foxter-brand-900")[1]
            if quartos_tag:
                quartos = quartos_tag.find('strong').get_text(strip=True)
                print(f"Quartos encontrados: {quartos}")
            else:
                print("Quartos não encontrados.")
                quartos = "N/A"

            # Vagas
            vagas_tag = anuncio.find_all('span', class_="whitespace-nowrap text-foxter-brand-900")[
                3]  # <- Corrigido para [3]
            if vagas_tag:
                vagas = vagas_tag.find('strong').get_text(strip=True)
                print(f"Vagas encontradas: {vagas}")
            else:
                print("Vagas não encontradas.")
                vagas = "0"

            # Valor
            valor_tag = anuncio.find('h1', class_="font-bold text-xl text-foxter-brand-700")
            if valor_tag:
                valor = valor_tag.get_text(strip=True)
                print(f"Valor encontrado: {valor}")
            else:
                print("Valor não encontrado.")
                valor = "N/A"

            # lista
            todos_imoveis.append({
                'Tipo': tipo,
                'Endereço': endereco,
                'Área': area,
                'Quartos': quartos,
                'Vagas': vagas,
                'Valor': valor
            })

        except Exception as e:
            print(f"Erro ao processar anúncio: {e}")
            continue

# DataFrame
df_imoveis = pd.DataFrame(todos_imoveis)

print(df_imoveis)

#show(df_imoveis)
