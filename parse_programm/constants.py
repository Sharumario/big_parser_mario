from pathlib import Path

BASE_DIR = Path(__file__).parent
BOOKS_CATEGORY = ['all', 'travel', 'mystery', 'classiccs']
BOOKS_PARSE_MODE = ['Css файл', 'Pretty табличка']
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
BOOKS_URL = 'http://books.toscrape.com/'
BOOKS_PAGE_URL = 'catalogue/page-{number_page}.html'
BOOKS_CATALOGUE_PAGE_URL = 'page-{number_page}.html'
PATTERN_ALL_PAGE_NUMBERS = r'\d+'
PATTERN_CATALOGUE = r'../../../([\w\-\/\.]+)'
PATTERN_IN_BRACKETS = r'\(([^\[\]]+)\)'
PATTERN_STAR_REITING = 'star-rating ([A-z]+)'
PROGRAMM_NAME = 'Большой парсер'
RATING_DICTIONARY = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
RESULTS_DIR = 'results'
WINDOW_SIZE = '700x450'
