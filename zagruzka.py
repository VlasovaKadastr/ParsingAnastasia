from datetime import datetime
import requests         # Для парсинга
from bs4 import BeautifulSoup         # Для парсинга
import schedule        #для таймера работы
import time        #для работы со временем
import re
URLKI = []          # Для хранения url
HTMLNAME = 'web_page.html'  # формируется для анализа оглавления раздела
OneParsing = True     # Для определения первого прохода
# Для поиска ключевых слов на странице
expressions = ["epublic", "emocratic"]
# Республиканская (Republican), демократическая (democratic)
html_file = "Analiz.html"  # формируется для анализа статьи

def PrintLog(Text):
    Text1 = f"{datetime.now()} -{Text}"
    print(Text1)
    with open(f"LogFail.txt", "a") as file:
        file.write(f"{Text1}\n")
def check_expressions_in_html(html_file, expressions):        # функция для происка слов в html странице
    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    found_expressions = []
    for expression in expressions:
        if expression in soup.get_text():
            found_expressions.append(expression)

    return found_expressions

def CreatHTML():   # функция для создания html файла
    global OneParsing
    url = "https://www.nytimes.com/section/politics"  # Замените на URL страницы, которую хотите сохранить
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        with open(HTMLNAME, "w", encoding="utf-8") as file:
            file.write(html_content)
        Text = (f"HTML-файл цели ({url}) успешно создан.")
        PrintLog(Text)
        ZapolnenitURLKI()   # вызов функции вытаскивающая уникальные URL с html страницы
        OneParsing = False
    else:
        Text = ("Не удалось загрузить страницу. Код состояния:", response.status_code)
        PrintLog(Text)

# В этой функции используется модуль re
# для работы с регулярными выражениями.
# Она ищет строки, содержащие заданный префикс и
# начинающиеся с "url":", а затем извлекает уникальные ссылки.
# Если совпадения найдены, они выводятся на экран.
# В приведенном примере выводятся две уникальные ссылки.
def find_matching_urls(html_content, prefix):
    pattern = r'"url":"(' + re.escape(prefix) + r'[^"]*)"'
    matching_urls = re.findall(pattern, html_content)
    unique_urls = list(set(matching_urls))
    return unique_urls

# Функция для чтения содержимого HTML файла с указанием кодировки UTF-8
def read_html_file(file_path):          # чтение html файла
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return html_content

def ZapolnenitURLKI():
    prefix = "https://www.nytimes.com/2024"      # уникальное значение для ссылок
    # https://www.nytimes.com/2024 типичное название для статей на текущем сайте
    html_content = read_html_file(HTMLNAME)      # чтение html файла
    matching_urls = find_matching_urls(html_content, prefix)       # анализ html файла на наличие ссылок
    i = 0
    if matching_urls:
        for url in matching_urls:
            if url not in URLKI:         # если значения нет в массиве url, то добавить
                if OneParsing == False:
                    Text = (f"Новый URL: {url}")
                    PrintLog(Text)
                    AnalizPars(url)
                    URLKI.append(url)
                else:
                    URLKI.append(url)
                    Text = (f"URL на момент старта: {url}")
                    PrintLog(Text)
                    AnalizPars(url)
            else:
                if i == 0:
                    Text = (f"Новые источники отсутствуют")
                    PrintLog(Text)
                    i = i + 1
    else:
        Text =("Совпадений не найдено.")
        PrintLog(Text)

def AnalizzHTML():
    # Opening the html file
    HTMLFile = open("Analiz.html", "r", encoding="utf-8")
    found = check_expressions_in_html(html_file, expressions)
    if found:
        for expression in found:
            Text = (f"Найденно выражение: {expression}")
            PrintLog(Text)
            # Reading the file
            index = HTMLFile.read()
            # Creating a BeautifulSoup object and specifying the parser
            S = BeautifulSoup(index, 'lxml')
            try:
                meta_tag1 = S.find('meta', property='og:title')
                NameStat = str(meta_tag1['content'])


                meta_tag2 = S.find('meta', property='og:description')
                Anotac = str(meta_tag2['content'])

                meta_tags = S.find_all("meta", attrs={"name": "byl"})

            # Извлекаем содержимое атрибута "content" для каждого найденного тега
                for meta_tag in meta_tags:
                    if "content" in meta_tag.attrs:
                        Autor = meta_tag["content"]
            except Exception as e:
                Text = (f"В статье выявленно два параметра!")
                PrintLog(Text)


            Text = (f"Название статьи: {NameStat}, Аннотация: {Anotac}, Имя автора: {Autor}.")
            PrintLog(Text)

    else:
        Text =("Ни одно из выражений не найдено в HTML файле.")
        PrintLog(Text)

def AnalizPars(url):
    # Ошибка 403 Forbidden указывает на то, что сервер понял запрос,
    # но отказывается его авторизовать из-за ограничений доступа.
    # Для обхода этой ошибки при парсинге веб-страницы можно попробовать следующий метод:
    # 1. **Использование заголовков User-Agent**:
    # Некоторые серверы могут блокировать запросы,
    # если они не содержат корректный заголовок User-Agent.
    # Вы можете попробовать установить заголовок User-Agent,
    # который имитирует браузер, например:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.text
        with open("Analiz.html", "w", encoding="utf-8") as file:
            file.write(html_content)
        Text =("Analiz.html успешно создан.")
        PrintLog(Text)
        AnalizzHTML()
    else:
        Text =(f"Не удалось загрузить страницу. Код состояния: {response.status_code}.")
        PrintLog(Text)



### Начинаем парсить
CreatHTML()
# Запланировать вызов основной функции каждые 10 минут minutes
schedule.every(10).minutes.do(CreatHTML)

# Запуск планировщика на протяжении 4 часов
for _ in range(4*6):  # 4 часа * 6 раз в часе запускается функция = 24 раза
    schedule.run_pending()
    time.sleep(10*60)  # Подождать 10 минут перед следующей итерацией, тут 60 - секунд умноженное на 10

Text = ("Прошло 4 часа. Программа завершена.")
PrintLog(Text)


