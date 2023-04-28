import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from pathlib import Path


def check_for_redirect(r):
    if r.history:
        raise requests.HTTPError


def parsing_book(book_id):
    url = f'https://tululu.org/b{book_id}'
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'lxml')
    title, author = soup.find('h1').text.split('::')
    return {'title': title.strip(), 'author': author.strip()}


def download_txt(book_id, folder='books/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    url = f'https://tululu.org/txt.php?id={book_id}'
    r = requests.get(url)
    r.raise_for_status()
    try:
        check_for_redirect(r)
        filename = ''.join((sanitize_filename(parsing_book(book_id)['title']), '.txt'))
        filepath = os.path.join(folder, filename)
        with open(filepath, 'w') as file:
            file.write(r.text)
        return filepath
    except requests.HTTPError:
        return f"book with id: {book_id} hasn't downloaded"


for i in range(1, 11):
    print(f'book {i}   ', download_txt(i))
