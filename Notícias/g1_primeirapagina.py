import requests
from bs4 import BeautifulSoup
import pandas as pd

lista_noticias = []

# requisição
response = requests.get('https://g1.globo.com/')

# conteudo da requisição
content = response.content

# converte conteudo em obj. BeautifulSoup
site = BeautifulSoup(content, 'html.parser')

# HTML para visualização.
#print(site.prettify())

# HTML da notícia
noticias = site.findAll('div', attrs={'class': 'feed-post-body'})

# coletar mais notícias
for noticia in noticias:

    #print(noticia.prettify())

    # Título
    titulo = noticia.find('a', attrs={'class': 'feed-post-link'})

    print(titulo.text)
    print(titulo['href']) # Link da noticia

    # Resumo: div class="feed-post-resumo"
    resumo = noticia.find('div', attrs={'class': 'feed-post-body-resumo'})

    if (resumo):
        print(resumo.text)
        lista_noticias.append([titulo.text, resumo.text, titulo['href']])
    else:
        lista_noticias.append([titulo.text, '', titulo['href']])

news = pd.DataFrame(lista_noticias, columns=['Manchete', 'Resumo', 'Link'])

news.to_excel('Noticias.xlsx', index=False)

print(news)