# -*- coding: Windows-1251 -*-
import requests
import time
import csv
from bs4 import BeautifulSoup


FILE = 'Wods.csv'
FILEERR = 'WodsErr.csv'
URL = 'http://ukrlit.org/slovnyk/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
page='радість'
WordDes=({'name':'Слово','description':'Визначення','link':'Посилання'})


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find('article', class_='word__description')== None: 
        description=None
        return description
    else: 
        description=soup.find('article', class_='word__description').get_text()
        return description.replace('\u0301','').replace('\u25ca','').replace('\u0463','і').replace('\u2206','/_\\').replace('\n','').replace('\t','')


def parse(url):
    html = get_html(url)# 404 chek
    if html.status_code == 200:
        worlds = get_content(html.text)
    else:
        print('Error')
        worlds=None
    return worlds


def save_file(item, path):
    with open(path, 'a', newline='',encoding='Windows-1251') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([item['name'], item['description'], item['link']])


#save_file(WordDes, FILE)
d = open("Zs1.csv", "r")
for i in d:  
    print(i)
    i=i.lower().replace('\n','').replace('?','')
    description=parse(URL+i)
    if description: 
        WordDes=({'name':i,'description':description,'link':URL+i})
        save_file(WordDes, FILE)
    else: 
        WordDes=({'name':i,'description':description,'link':description})
        save_file(WordDes, FILEERR)
    time.sleep(1)
d.close()
