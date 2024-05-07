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

# if the searched term leads directly to an article, returns the url of the article, otherwise prints a list of search results
# the user chooses from the results, the chosen url is returned
# term: the search term
# return: an url, to be passed to one of the retrieve functions
def search(term):
    searchterm = term.replace(' ', '+')

    search_url = f'https://en.wikipedia.org/w/index.php?search={searchterm}'

    results_page = requests.get(search_url)

    if results_page.status_code == 200:
        parsed_res_page = BeautifulSoup(results_page.content, 'html.parser')

        type_of_result = parsed_res_page.find('title')
        if 'Search results' not in type_of_result.getText():
            print('article found')
            return search_url
        
        res_list = parsed_res_page.find("div", {"class":"mw-search-results-container"}).find("ul").findAll("li")

        results = []
        links = []

        for res in res_list:
            link = res.find('a').get('href')
            result = res.find('a').get('title')

            results.append(result)
            links.append(f'https://en.wikipedia.org{link}')

        counter = 0
        for result in results:
            print(f'{counter}. {result}')
            print(links[counter])
            print('\n')
            counter += 1

        #print(results)
        

        while True:
            try:
                numinp = input('select a number from the listed entries: ')
                link = links[int(numinp)]
                return link
            except ValueError:
                print('invcalid input')

running = True
while running:
    searchterm = input('what do you want to search for?\n')

    url = search(searchterm)

    mode = input('sources or text?\n')
    if mode == 'sources':
        retrieve_article_sources(url)
    else:
        retrieve_article_text(url)