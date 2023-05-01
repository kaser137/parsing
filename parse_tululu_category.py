import requests
import argparse
import os
import json
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
from time import sleep
import parse_tululu


def main():
    parser = argparse.ArgumentParser(description='Getting books')
    parser.add_argument('-s', '--start_page', type=int, default=1,
                        help='page for start, must be >= 1')
    parser.add_argument('-e', '--end_page', type=int, default=701,
                        help='page for end, must be >= start_id')
    args = parser.parse_args()
    for page in range(args.start_page, args.end_page + 1):
        url = f'https://tululu.org/l55/{page}/'
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        books_on_page = soup.select('.d_book ')
        for book in books_on_page:
            # bookpath = urljoin(response.url, book.select_one('a')['href'])
            book_id = book.select_one('a')['href'][2:-1]
            url = f'https://tululu.org/b{book_id}/'
            try:
                book_details = parse_tululu.parse_book_page(parse_tululu.get_response(url))
                parse_tululu.download_txt(book_id, book_details['title'])
                parse_tululu.download_img(book_details['img'])
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
                    file.write(books_json + ',\n')
                print(url)
            except requests.HTTPError:
                print(f'book with number {book_id} is absent')


if __name__ == '__main__':
    main()
