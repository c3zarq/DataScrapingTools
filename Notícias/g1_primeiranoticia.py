import requests
from bs4 import BeautifulSoup

# requisição
response = requests.get('https://g1.globo.com/')

# conteudo da requisição
content = response.content

# converte conteudo para obj. BeautifulSoup
site = BeautifulSoup(content, 'html.parser')

# HTML visualização.
#print(site.prettify())

# HTML da notícia
noticia = site.find('div', attrs={'class': 'feed-post-body'})

print(noticia.prettify())

# Título
titulo = noticia.find('a', attrs={'class': 'feed-post-link'})

print(titulo.text)

# Resumo: div class="feed-post-resumo"
resumo = noticia.find('div', attrs={'class': 'feed-post-body-resumo'})

print(resumo.text)