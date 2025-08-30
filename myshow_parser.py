import requests
from bs4 import BeautifulSoup
import pandas as pd

def collect_user_rates(user_login):
    data = []

    url = f'https://myshows.me/{user_login}/wasted/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    entries = soup.find_all('div', class_='ShowCol__cell')

    for entry in entries:
        ru_title = entry.find('div', class_='ShowCol-title')
        ru_name = ru_title.find('a').text

        orig_title = entry.find(class_='ShowCol-titleOriginal')
        if orig_title is not None:
            original_name = orig_title.text
        else:
            original_name = ru_name

        show_rate = entry.find('div', class_='Rating Rating--disabled Rating--active Rating--size-s mobile tablet')
        if show_rate:
            rate1 = show_rate.find('div', class_='Rating__wrapper')
            rate = rate1.get('title')
        else:
            rate = 0

        data.append({'Сериал(название на русском)': ru_name, 'Сериал(ориг. название)': original_name, 'Рейтинг пользователя': rate})
    r_data = list(filter(lambda x: x['Рейтинг пользователя'] != 0, data))
    return r_data

user_rates = collect_user_rates(user_login='Nog')
df = pd.DataFrame(user_rates)

df.to_excel('user_rates.xlsx')
