import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote


def check_for_redirect(r):
    if r.history:
        raise requests.HTTPError


def get_response(url, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    return response


def parse_book_page(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    title, author = soup.find('h1').text.split('::')
    img = urljoin('https://tululu.org/', soup.find(class_='bookimage').find('img')['src'])
    comments = soup.find_all(class_='texts')
    genres = soup.find('span', class_='d_book').find_all('a')
    return {
        'title': title.strip(),
        'author': author.strip(),
        'img': img,
        'comments': [comment.find(class_='black').text for comment in comments],
        'genres': [genre.text for genre in genres]
    }


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



