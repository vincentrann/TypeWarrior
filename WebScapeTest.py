import requests
from bs4 import BeautifulSoup

main_url = 'https://data.typeracer.com/pit/texts'
page = requests.get(main_url)
all_quotes = []

def getdata(url):
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def gettext(url):
    text_url = url
    text_page = requests.get(text_url)
    soup = BeautifulSoup(text_page.content, 'html.parser')
    words = soup.find('div', {'class':'fullTextStr'})
    if text_page.text.count('English') == 1 and words != None:
        return words.text
    else:
        return None


def database(soup):
    containers = soup.findAll('td', {"style":"text-align: left;"})
    urls = []

    for container in containers:
        if not container.a.has_attr('class'):
            url = 'https://data.typeracer.com/pit/' + str(container.a['href'])
            urls.append(url)

    return urls

def check_string(file_name, string):
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if string in line:
                return True
    return False


data = getdata(main_url)
urls = database(data)

for i in range(0,10):
    all_quotes.append(gettext(urls[i]))

with open('AllTexts.txt', 'a') as f:
    for line in all_quotes:
        if line != None and not check_string('AllTexts.txt', line):
            f.write(line)
            f.write('\n')






















