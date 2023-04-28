import requests
import argparse
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
from time import sleep


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_response(url, params=None, attempt_timeout=5):
    flag = True
    while flag:
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            check_for_redirect(response)
            flag = False
            return response
        except requests.exceptions.ConnectionError or requests.exceptions.Timeout:
            print(f'connection failed, next attempt in {attempt_timeout} seconds')
            sleep(attempt_timeout)


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title, author = soup.find('h1').text.split('::')
    img_src = urljoin(response.url, soup.find(class_='bookimage').find('img')['src'])
    comments = soup.find_all(class_='texts')
    genres = soup.find('span', class_='d_book').find_all('a')
    return {
        'title': title.strip(),
        'author': author.strip(),
        'img': img_src,
        'comments': [comment.find(class_='black').text for comment in comments],
        'genres': [genre.text for genre in genres]
    }


def download_txt(book_id, name, folder='books/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    url = f'https://tululu.org/txt.php'
    params = {'id': book_id}
    response = get_response(url, params=params)
    filename = f'{sanitize_filename(name)}.txt'
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w') as file:
        file.write(response.text)
    return filepath


def download_img(url, folder='images/'):
    Path(Path.cwd() / folder).mkdir(parents=True, exist_ok=True)
    filename = unquote(urlsplit(url).path).split('/')[-1]
    response = get_response(url)
    filepath = os.path.join(folder, sanitize_filename(filename))
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def main():
    parser = argparse.ArgumentParser(description='Getting books')
    parser.add_argument('start_id', nargs='?', type=int, default=1,
                        help='book_id for start, must be >= 1')
    parser.add_argument('end_id', nargs='?', type=int, default=10,
                        help='book_id for end, must be >= start_id')
    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id+1):
        url = f'https://tululu.org/b{book_id}/'
        try:
            book_details = parse_book_page(get_response(url))
            download_txt(book_id, book_details['title'])
            download_img(book_details['img'])
        except requests.HTTPError:
            print(f'book with number {book_id} is absent')


if __name__ == '__main__':
    main()
