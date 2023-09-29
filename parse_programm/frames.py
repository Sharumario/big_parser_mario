import re
import tkinter as tk
from tkinter import SINGLE, ttk
from urllib.parse import urljoin

import requests_cache
from constants import (BOOKS_CATALOGUE_PAGE_URL, BOOKS_CATEGORY,
                       BOOKS_PAGE_URL, BOOKS_URL, PATTERN_ALL_PAGE_NUMBERS,
                       PATTERN_CATALOGUE, PATTERN_IN_BRACKETS,
                       PATTERN_STAR_REITING, RATING_DICTIONARY)
from utils import get_output_file_csv, get_soup


class Menu(ttk.Frame):
    """"Класс создания меню программы."""
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.grid(row=0, column=0, sticky='nsew')
        self.main_frame = DescriptionFrame()

    def create_widgets(self):
        menu_head_label = ttk.Label(
            self,
            text='Выберите категорию для парсинга'
        )
        button_description = ttk.Button(
            self,
            text='Описание',
            command=lambda: self.create_main_field('Описание')
        )
        button_books = ttk.Button(
            self,
            text='Книги',
            command=lambda: self.create_main_field('Книги')
        )
        frame_2_button = ttk.Button(self, text='Тачки')

        menu_head_label.grid(row=0, column=0, padx=20, pady=20)
        button_description.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        button_books.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        frame_2_button.grid(row=3, column=0, sticky='ew', padx=5, pady=5)

    def create_main_field(self, name):
        self.main_frame.destroy()
        if name == 'Описание':
            self.main_frame = DescriptionFrame()
        if name == 'Книги':
            self.main_frame = BooksFrame()


class DescriptionFrame(ttk.Frame):
    """"Класс описывающий работу программы"""
    def __init__(self):
        super().__init__()
        self.home_frame_label = ttk.Label(
            self,
            text='Добро пожаловать в большой парсер для 10 тестовых сайтов,\n'
            'работающий на библиотеках tkinter, request_cashed, bs4'
        )
        self.home_frame_label.grid(padx=20, pady=20)
        self.grid(row=0, column=1, sticky="nsew")


class BooksFrame(DescriptionFrame):
    """"Класс создающий сруктуру для парсинга книг с сайта
    http://books.toscrape.com/index.html"""
    def __init__(self):
        super().__init__()
        self.home_frame_label.config(
            text='В данном разделе вы можете спарсить информацию с сайта\n'
            'http://books.toscrape.com/index.html. Выберите категорию и\n'
            'режим парсера, после нажмите Спарсить. По истечение загрузки\n'
            'рядом с файлом программы создаётся папка с файлом csv'
        )
        self.session = requests_cache.CachedSession()
        self.create_parser_elements()

    def create_parser_elements(self):
        soup = get_soup(self.session, BOOKS_URL)
        category = [
            tag.text.strip().lower() for tag in soup.select(
                'div.side_categories li a'
            )
        ]
        self.list_box_change_category = tk.Listbox(
            self,
            selectmode=SINGLE,
            exportselection=0
        )
        self.list_box_change_category.insert(0, *BOOKS_CATEGORY)
        self.progress_bar_parse = ttk.Progressbar(
            self,
            orient=tk.HORIZONTAL
        )
        self.button_parse = ttk.Button(
            self, text='Спарсить', command=self.run_parser)

        self.list_box_change_category.grid(row=1, padx=25, pady=25)
        self.progress_bar_parse.grid()
        self.button_parse.grid()

    def run_parser(self):
        self.button_parse.configure(state=['disable'])
        if (
            BOOKS_CATEGORY[self.list_box_change_category.curselection()[0]]
        ) == 'all':
            get_output_file_csv(self.parse_category_books('all'), 'all')
        if (BOOKS_CATEGORY[
            self.list_box_change_category.curselection()[0]
        ]) == 'travel':
            get_output_file_csv(self.parse_category_books('travel'), 'travel')
        if (BOOKS_CATEGORY[
            self.list_box_change_category.curselection()[0]
        ]) == 'mystery':
            get_output_file_csv(self.parse_category_books('mystery'), 'mystery')
        self.progress_bar_parse.configure(value=0)
        self.button_parse.configure(state=['enable'])

    def parse_category_books(self, category):
        result = []
        soup = get_soup(self.session, BOOKS_URL)
        if category != 'all':
            category_url = [tag for tag in soup.select(
                        'div.side_categories li a'
                    )
                     if tag.text.strip().lower() == category][0]['href']
            soup = get_soup(self.session, urljoin(BOOKS_URL, category_url))
        pages_str = soup.select('ul li.current')
        if pages_str:
            count_page = re.findall(
                PATTERN_ALL_PAGE_NUMBERS, pages_str[0].text
            )
            first_page, last_page = int(count_page[0]), int(count_page[1])
            self.progress_bar_parse.configure(maximum=last_page)
            pages_url = [
                urljoin(
                    BOOKS_URL,
                    BOOKS_PAGE_URL.format(number_page=number_page)
                    if category == 'all' else category_url[:-10] +
                    BOOKS_CATALOGUE_PAGE_URL.format(number_page=number_page)
                )
                for number_page in range(first_page, last_page+1)
            ]
        else:
            pages_url = [urljoin(BOOKS_URL, category_url)]
            self.progress_bar_parse.configure(maximum=1)
        for num, page_url in enumerate(pages_url):
            soup = get_soup(self.session, page_url)
            self.progress_bar_parse.configure(value=num+1)
            self.update()
            for section in soup.select('div.image_container'):
                url = section.find('a')['href']
                version_link = urljoin(
                    BOOKS_URL+'catalogue/',
                    re.findall(PATTERN_CATALOGUE, url)[0]
                ) if category != 'all' else urljoin(
                    BOOKS_URL,
                    (url if url[:9] == 'catalogue' else 'catalogue/' + url)
                )
                soup = get_soup(self.session, version_link)
                result.append(
                    [
                        soup.find('h1').text,
                        soup.select('ul.breadcrumb li')[2].text.strip(),
                        float(soup.find('p', class_='price_color').text[1:]),
                        int(re.findall(PATTERN_IN_BRACKETS, soup.find(
                            'p', class_='instock availability'
                        ).text)[0].split()[0]),
                        RATING_DICTIONARY[
                            re.findall(PATTERN_STAR_REITING, str(soup))[0]
                        ]
                    ]
                )
        result.sort(key=lambda x: x[2])
        return [
            [
                'Название книги', 'Жанр', 'Цена(Евро)',
                'Количество книг', 'Рейтинг'
            ],
            *result,
            ['Минимальная цена(Евро)', result[0][0], result[0][2]],
            ['Максимальная цена(Евро)', result[-1][0], result[-1][2]]
        ]
