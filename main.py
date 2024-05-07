import webscraper as ws

running = True
while running:
    searchterm = input('what do you want to search for?\n')

    url = ws.search(searchterm)

    mode = input('sources or text?\n')
    if mode == 'sources':
        ws.retrieve_article_sources(url)
    else:
        ws.retrieve_article_text(url)