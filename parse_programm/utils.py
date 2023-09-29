import csv
import datetime as dt
from threading import Thread

from bs4 import BeautifulSoup
from constants import BASE_DIR, DATETIME_FORMAT, RESULTS_DIR
from requests import RequestException


def get_output_file_csv(result, category):
    results_dir = BASE_DIR / RESULTS_DIR
    results_dir.mkdir(exist_ok=True)
    now = dt.datetime.now()
    now_formated = now.strftime(DATETIME_FORMAT)
    file_name = f'БД_{category}_книги {now_formated}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        csv.writer(f, dialect=csv.unix_dialect).writerows(result)


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        raise ConnectionError('ошибка соединения')


def get_soup(session, url, features='lxml'):
    return BeautifulSoup(get_response(session, url).text, features)


def thread(function):
    def wrapper(*args, **kwargs):
        thread = Thread(target=function, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper
