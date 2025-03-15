import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd

options = Options()
options.add_argument('window-size=400,800')

navegador = webdriver.Chrome(options)

url = 'https://www.airbnb.com.br/'
navegador.get(url)

sleep(2)

cl1 = navegador.find_element(by=By.TAG_NAME, value='button')
cl1.click()

sleep(0.5)

cl2 = navegador.find_element(by=By.CSS_SELECTOR, value="span.lspkrbu")
cl2.click()

sleep(0.5)

buscador = navegador.find_element(by=By.CSS_SELECTOR, value="input.ixu4gk5")
buscador.send_keys('São Paulo')
buscador.submit()

sleep(0.5)

pular_data = navegador.find_element(by=By.CSS_SELECTOR, value='div.bs992qt')
pular_data.click()

sleep(0.5)

adultos = navegador.find_element(by=By.CSS_SELECTOR, value='button:nth-child(3) > span > svg')
adultos.click()
adultos.click()

sleep(0.5)

ir_para_lista = navegador.find_element(by=By.CSS_SELECTOR, value='span.tmel3e0')
ir_para_lista.click()

sleep(4)

page_content = navegador.page_source

site = BeautifulSoup(page_content, 'html.parser')

dados_hospedagens = []

hospedagens = site.findAll('div', attrs={'itemprop': 'itemListElement'})

c = 0

for hospedagem in hospedagens:
    hospedagem_tipo = hospedagem.find('div', attrs={'data-testid':'listing-card-title'})
    hospedagem_url = hospedagem.find('meta', attrs={'itemprop': 'url'})
    hospedagem_descr = hospedagem.find('span', attrs={'data-testid': 'listing-card-name'})
    hospedagem_preco = hospedagem.find('span', attrs={'class': '_1y74zjx'})
    c = c + 1

    print('-=-='* 40)
    print('')
    print(f'[{c}]')
    print('Tipo: ', hospedagem_tipo.text)
    print('URL: ', hospedagem_url['content'])
    print('Descrição: ', hospedagem_descr.text)
    print('Preço: ', hospedagem_preco.text)
    print('')

    dados_hospedagens.append([hospedagem_tipo.text, hospedagem_url['content'], hospedagem_descr.text, hospedagem_preco.text])

print(f'[{c}] resultados encontrados')

dados = pd.DataFrame(dados_hospedagens, columns=['Tipo', 'URL', 'Descrição', 'Preço'])
dados.to_excel('hospedagens.xlsx', index=False)