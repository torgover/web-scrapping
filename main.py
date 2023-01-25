from bs4 import BeautifulSoup
import requests
from fake_headers import Headers
import pprint
import time
import json

HOST = 'https://spb.hh.ru/search/vacancy?text={text}&area=1&area=2'
def get_headers():
    return Headers(browser='chrome', os='win').generate()

    
def get_link(text):
    data = requests.get(url=f'https://spb.hh.ru/search/vacancy?text={text}&area=1&area=2', 
                        headers=get_headers())
    if data.status_code != 200:
        return
    
    soup = BeautifulSoup(data.text, features='lxml')
    try:
        count_page = int(soup.find('div', class_='pager').find_all('span', recursive=False)[-1].find('a').find('span').text)
    except:
        return
    for page in range(count_page):
        try:
            data = requests.get(
                url=f'https://spb.hh.ru/search/vacancy?text={text}&area=1&area=2&page={page}', 
                headers=get_headers()
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, 'lxml')
            for  a in soup.find_all('a', attrs={'serp-item__title'}):
                yield f"{a.attrs['href'].split('?')[0]}"   
        except Exception as e:
            print(f"{e}")
        time.sleep(1)

def get_resume(link):
    data = requests.get(
        url=link,
        headers=get_headers()
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, 'lxml')
    try:
        name = soup.find(attrs={'class':'bloko-header-section-1'}).text
    except:
        name = ''
    try:
        salary = soup.find(attrs={'class':'bloko-header-section-2 bloko-header-section-2_lite'}).text
    except:
        salary = ''
    try:
        name_company = soup.find(attrs={'class':'vacancy-company-details'}).text
    except:
        name_company = ''
    try:
        city = soup.find(attrs={'data-qa':'vacancy-view-location'}).text
    except:
        city = ''
    resume = {
        'name':name,
        'salary':salary,
        'name_company':name_company,
        'city':city
    }
    return resume



if __name__ == '__main__':
    data = []             
    for a in get_link('python'):
        data.append(get_resume(a))
        time.sleep(1)
        with open('resume.json', 'w', encoding='utf-8') as f:
            json.dump(data,f,indent=4,ensure_ascii=False)
