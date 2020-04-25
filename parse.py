#!C:\Users\Peter\Downloads python3

import requests
import csv
from bs4 import BeautifulSoup

result=[]
BASE_URL='https://www.weblancer.net/jobs/'

def get_html(url):
    response=requests.get(url)
    return response.text

def get_pages_count(html):
    soup=BeautifulSoup(html)
    paggination = soup.find('div','pagination_box')
    a = paggination.findAll('a')[-1].get('href').split('=')[-1]
    return int(a)

def save(projects,path):
    with open(path,'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Проект', 'Описание', 'Цена', 'Заявок'))
        for project in projects:
            writer.writerow((project['title'], project['text'], project['price'], project['appls']))


def parse(html):
    soup=BeautifulSoup(html,'html.parser')
    table = soup.findAll('div','cols_table')
    rows=[]
    for i in table:
        tmp=i.findAll('div','row')
        for j in tmp:
            rows.append(j)
    rows=rows[2:-2:]
    td=[]
    for i in rows:
        td.append(i.find('div','col-sm-10'))
    projects=[]
    for i in td:
        projects.append({
            'title':i.h2.text,
            'text': i.p.text
            })
    td=[]
    for i in rows:
        td.append(i.find('div','col-sm-2'))
    for i in range(len(projects)):
        projects[i]['price'] = td[i].find('div','amount').text
        projects[i]['appls'] = td[i].find('div','text_field').text.strip()

    return projects

def main():
    page_count = get_pages_count(get_html(BASE_URL))
    print(f'Всего найдено страниц {page_count}')

    for i in range(1,page_count+1):
        print(f'Парсинг {i/page_count*100}%')
        result.extend(parse(get_html(BASE_URL + f'?page={i}')))
            
    save(result,'db.csv')

if __name__=='__main__':
    main()
