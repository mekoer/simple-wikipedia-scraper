import requests
import re
from tkinter import Tk
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

def is_list_element(tag):
    return tag.name == "div" and re.match()

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
        #article_text = re.sub(r'\[[0-9]+\]', '', article_text)
        #article_text = re.sub(r'\[[a-z]+\]', '', article_text)

        

running = True
while running:
    #command = input()
    #command = command.split(' ')

    #article_search_term = command[1]
    #article_search_term.replace(' ', '_')
    url = 'https://en.wikipedia.org/wiki/Danube'
    retrieve_article_sources(url)



    running = False

    #if command[0] == 'text':
     #   retrieve_article_text(url)
    #if command[0] == 'sources':
     #   retrieve_article_sources(url)

