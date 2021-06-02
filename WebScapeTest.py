import requests
from bs4 import BeautifulSoup

main_url = 'https://data.typeracer.com/pit/texts'
page = requests.get(main_url)
all_texts = []

def getdata(url):
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def gettext(url):
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def textpage(soup):
    containers = soup.findAll('td', {"style":"text-align: left;"})
    urls = []

    for container in containers:
        if not container.a.has_attr('class'):
            url = 'https://data.typeracer.com/pit/' + str(container.a['href'])
            urls.append(url)

    return urls


data = getdata(main_url)
urls = textpage(data)

'''for url in urls:
    all_texts.append(gettext(url))

print(all_texts)'''














