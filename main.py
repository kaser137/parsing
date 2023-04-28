import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote


def check_for_redirect(r):
    if r.history:
        raise requests.HTTPError


def get_response(url, params={}):
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    return response


def parsing_book(book_id):
    url = f'https://tululu.org/b{book_id}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    title, author = soup.find('h1').text.split('::')
    img = urljoin('https://tululu.org/', soup.find(class_='bookimage').find('img')['src'])
    return {'title': title.strip(), 'author': author.strip(), 'img': img}


def download_txt(book_id, name, folder='books/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    url = f'https://tululu.org/txt.php?id={book_id}'
    r = get_response(url)
    filename = f'{sanitize_filename(name)}.txt'
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w') as file:
        file.write(r.text)
    return filepath


def download_img(url, folder='images/'):
    Path(Path.cwd() / folder).mkdir(parents=True, exist_ok=True)
    filename = unquote(urlsplit(url).path).split('/')[-1]
    r = get_response(url)
    filepath = os.path.join(folder, sanitize_filename(filename))
    with open(filepath, 'wb') as file:
        file.write(r.content)
    return filepath



for i in range(1,11):
    try:
        url = f'https://tululu.org/txt.php?id={i}'
        r = get_response(url)
        download_img(parsing_book(i)['img'])
    except requests.HTTPError:
        continue
