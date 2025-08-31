# myshow_parser
HW_23.2.1
---

Построить парсер, принимающий уникальный идентификатор пользователя Myshows, возвращающий информацию об оценках сериалов этим пользователем.
Горизонтально расширяя такой парсер мы смогли бы в перспективе построить улучшенную версию рекомендательной системы сериалов, которая будет основываться на множестве разных сервисов-социальных сетей для любителей сериалов.

---
* Загружаем библиотеки, которы нам понадобятся для работы кода:
`
pip install beautifulsoup4 lxml
`
`
pip install pandas openpyxl
`
* Импортируем эти библиотеки в код:
```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
```
* Создаем функцию для работы парсера:
```python
def collect_user_rates(user_login):
```
* Реализованную функцию можно будет интегрировать в потенциальный класс, который будет решать множество задач парсинга Myshows.

* Выбираем пользователя (Nog) платформы [myshows](https://myshows.me/) и переходим на [страницу с его оценками](https://myshows.me/Nog/wasted/).
* Выгружать будем 3 позиции:
  1) Название сериала на русском языке
  2) Оригинальное название сериала (т.к. перевод может разниться на других платформах)
  3) Оценка пользователя
* Создаем пустой список для этих данных:
```python
data = []
```

* Cоздаем объект для отправки запросов и объект BeautifulSoup, которому будет передаваться ответ на запрос и указываем, что для парсинга необходимо использовать lxml:
```
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
```

* Проанализировав код, находим нужные нам контейнеры и получаем элементы:
```python
entries = soup.find_all('div', class_='ShowCol__cell')
```
* Для этого пройдемся по всем элементам, выгруженных контейнеров:
```python
   for entry in entries:
        ru_title = entry.find('div', class_='ShowCol-title')
        ru_name = ru_title.find('a').text
```
* Оригинальные названия есть не во всех контейнерах, поэтому добаляем условия вхождения:
```python
        orig_title = entry.find(class_='ShowCol-titleOriginal')
        if orig_title is not None:
            original_name = orig_title.text
        else:
            original_name = ru_name
```
* Оценки тоже есть не везде, т.к. в списке есть чериалы, которые пользователь посмотрел не до конца или перестал смотреть:
```python
        show_rate = entry.find('div', class_='Rating Rating--disabled Rating--active Rating--size-s mobile tablet')
        if show_rate:
            rate1 = show_rate.find('div', class_='Rating__wrapper')
            rate = rate1.get('title')[-1]
        else:
            rate = 0
```
* Получив все данные добавлем их список:
```python
data.append({'Сериал(название на русском)': ru_name, 'Сериал(ориг. название)': original_name, 'Рейтинг пользователя': rate})
```
* Фильтруем наш список, убирая все сериалы без оценок и возвращаем его:
```python
    r_data = list(filter(lambda x: x['Рейтинг пользователя'] != 0, data))
    return r_data
```
* Вводим имя пользователя:
```python
user_rates = collect_user_rates(user_login='Nog')
```
* Экпортируем данные в Excel:
```python
df = pd.DataFrame(user_rates)

df.to_excel('user_rates.xlsx')
```
* В результате вы обеспечили не только извлечение данных но и представление их в удобной форме для дальнейшего взаимодействия с ними.:
(https://github.com/Nuselda/myshow_parser/blob/master/user_rates.xlsx)
