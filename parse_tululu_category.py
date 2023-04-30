import requests
import argparse
import os
import json
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
from time import sleep
import main


books_info = []
for i in range(1, 11):
    url =f'https://tululu.org/l55/{i}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    books_on_page = soup.find_all(class_='d_book')
    for book in books_on_page:
        bookpath = urljoin(response.url, book.find('a')['href'])
        book_id = book.find('a')['href'][2:-1]
        url = f'https://tululu.org/b{book_id}/'
        try:
            book_details = main.parse_book_page(main.get_response(url))
            main.download_txt(book_id, book_details['title'])
            main.download_img(book_details['img'])
            book_info = {
                'title': book_details['title'],
                'author': book_details['author'],
                'imc_src': f'images/{unquote(urlsplit(book_details["img"]).path).split("/")[-1]}',
                'book_path': f'books/{sanitize_filename(book_details["title"])}.txt',
                'comments': book_details['comments'],
                'genres': book_details['genres'],
            }
            books_json = json.dumps(book_info, indent=0, ensure_ascii=False, separators=(', ', ': '))
            with open('books.json', 'a', encoding='utf8') as file:
                file.write(books_json+',\n')
        except requests.HTTPError:
            print(f'book with number {book_id} is absent')


