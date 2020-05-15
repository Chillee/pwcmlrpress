import requests
from bs4 import BeautifulSoup
import re
import json

all_confs = []
lowest_conf = 30
r = requests.get(f'http://proceedings.mlr.press')
soup = BeautifulSoup(r.text, 'html.parser')
proceedings_list = soup.select('#content > .wrapper > .proceedings-list')[1]
confs = proceedings_list.select('li > a')
for conf in confs:
    vol = int(conf['href'][1:])
    if vol < lowest_conf:
        continue
    r = requests.get(f'http://proceedings.mlr.press/v{vol}/')
    if r.status_code != requests.codes.ok:
        pass
    soup = BeautifulSoup(r.text, 'html.parser')
    conf_info = soup.select('#content > div > h2')[0].text
    conf_info = re.search('Volume \d*: (.*)', conf_info).group(1).split(',')
    conf_name = conf_info[0].strip()
    date = conf_info[1].strip()
    print(conf_name, date)
    papers = soup.findAll('div', class_='paper')
    all_info = []
    for paper in papers:
        info = {}
        info['title'] = paper.find('p', class_='title').text
        authors = paper.find('span', class_='authors').text.split(',')
        authors = [i.strip() for i in authors]
        info['authors'] = authors
        links = paper.find('p', class_='links').findAll('a')

        mapping = {
            'download pdf': 'pdf_link',
            'abs': 'abstract',
            'code': 'code'
        }
        for k in mapping.values():
            info[k] = None
        for i in links:
            key = i.text.strip().lower()
            if key in mapping:
                info[mapping[key]] = i['href']
        all_info.append(info)
    parsed_conf_info = {
        'conf_name': conf_name,
        'date': date,
        'papers': all_info,
    }
    all_confs.append(parsed_conf_info)

json.dump(all_confs, open('mlrpress.json', 'w'), indent=2, sort_keys=True)