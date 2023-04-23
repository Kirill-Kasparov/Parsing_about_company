import requests    # by Kirill Kasparov, 2022
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_about_company(url):
    if 'https://' not in url:
        url = 'https://' + str(url)
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.title
        description = soup.find('meta', {'name': 'description'})
        if str(description) != 'None':
            description = description.get('content')
        else:
            description = ''
        about_company = title.text + '. ' + str(description)
        return about_company
    else:
        return False

# Тело кода
data_import = os.getcwd().replace('\\', '/') + '/' + 'import.csv'
data_export = os.getcwd().replace('\\', '/') + '/' + 'export_about_company.csv'

df = pd.read_csv(data_import, sep=';', encoding='windows-1251', nrows=200000)
df['website'] = df['website'].fillna('0')
df['website'] = df['website'].astype('str')

about_company = []
count = 0
for site in df['website']:
    about_company.append(get_about_company(site))
    count += 1
    print('Обработано:', count, 'из', len(df['website']))

df['about_company'] = about_company
df.to_csv(data_export, sep=';', encoding='windows-1251', index=False, mode='w')
print('Данные сохранены в файл:', data_export)
