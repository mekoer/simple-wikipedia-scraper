import requests
import re
from bs4 import BeautifulSoup

def retrieve_article_text(url):
    response = requests.get(url)

    if response.status_code == 200:
        parsed_html = BeautifulSoup(response.content, 'html.parser')
        article_div = parsed_html.find('div', id='mw-content-text')
        article_text = article_div.findAll('p')

        for paragraph in article_text:
            par_text = paragraph.getText()
            if par_text != '' and par_text != '\n':
                par_text = re.sub(r'\[[0-9]+\]', '', par_text)
                par_text = re.sub(r'\[[a-z]+\]', '', par_text)
                print(par_text)


def retrieve_article_sources(url):
    response = requests.get(url)

    if response.status_code == 200:
        parsed_html = BeautifulSoup(response.content, 'html.parser')
        article_ref_div = parsed_html.find('div', {"class":'reflist'})
        article_ref_list = (article_ref_div.find("ol", {"class":"references"})).findAll("li")

        counter = 1

        for ref in article_ref_list:
            try:
                link = ref.find("span", {"class":"reference-text"}).find("a").get("href")
                print(ref.getText().replace("\n", "").replace("^ ", f"{counter}. "))
                print(link)
                print('\n')
                counter += 1
            except AttributeError: 
                print(f'{counter}. error')
                counter += 1
                continue

        

running = True
while running:
    searchterm = 'objective oriented programming'
    searchterm = searchterm.replace(' ', '+')

    search_url = f'https://en.wikipedia.org/w/index.php?search={searchterm}'

    results_page = requests.get(search_url)

    if results_page.status_code == 200:
        parsed_res_page = BeautifulSoup(results_page.content, 'html.parser')
        
        res_list = parsed_res_page.find("div", {"class":"mw-search-results-container"}).find("ul").findAll("li")

        links = []
        results = []

        for res in res_list:
            links.append(res.find('a').get('href'))
            results.append(res.find('a').get('title'))

    counter = 0
    for result in results:
        print(result)
        print(f'https://en.wikipedia.org/wiki/{links[counter]}')
        print('\n')
        counter += 1

    running = False
    # url = 'https://en.wikipedia.org/wiki/Danube'
    # retrieve_article_text(url)

    

