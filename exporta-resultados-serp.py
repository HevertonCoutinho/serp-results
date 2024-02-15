import csv
import urllib.parse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Função para rolar até o final da página de forma contínua
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Aguarde para carregar os resultados
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Palavras-chave para pesquisa
pesquisa = input('Digite sua busca: ')
num_results = int(input('Digite o número de resultados por página: '))
intervalo = int(input('Digite o intervalo de tempo entre as requisições (em segundos): '))

# Codifica as palavras-chave
query = urllib.parse.quote_plus(pesquisa)

# URL da página de resultados de pesquisa
url = f'https://www.google.com/search?q={query}&num={num_results}'

# Inicialize a lista de resultados da pesquisa
results = []

# Configure o WebDriver para o Chrome
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)

# Aguarde até que a página esteja totalmente carregada
driver.get(url)
wait = WebDriverWait(driver, 5)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#search')))

# Enquanto houver rolagem, extraia os URLs dos resultados da pesquisa
while True:
    # Encontrar todos os links na página com a tag <a>
    links = driver.find_elements(By.CSS_SELECTOR, 'div#search a')
    
    # Extrair os URLs dos resultados da pesquisa e adicioná-los à lista de resultados
    for link in links:
        url = link.get_attribute('href')
        if url and url.startswith('http'):
            results.append(url)
    
    # Exporte os URLs para um arquivo CSV
    with open('resultados.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for url in results:
            writer.writerow([url])
    
    # Role até o final da página
    scroll_to_bottom(driver)
    
    # Verifique se há mais resultados além da rolagem atual
    more_results = driver.find_elements(By.CSS_SELECTOR, 'div#search div[data-async-rclass="search"]')
    
    if not more_results:
        break
    
    # Aguarde até que a próxima página esteja totalmente carregada
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#search')))

    time.sleep(intervalo)  # Adiciona um tempo de espera definido pelo usuário entre cada solicitação

# Feche o WebDriver
driver.quit()
