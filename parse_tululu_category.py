import requests
import argparse
import json
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from pathlib import Path
from urllib.parse import urlsplit, unquote
import parse_tululu


def main():
    parser = argparse.ArgumentParser(description='Getting books')
    parser.add_argument('-s', '--start_page', type=int, default=1,
                        help='page for start, must be >= 1')
    parser.add_argument('-e', '--end_page', type=int, default=701,
                        help='page for end, must be >= start_id')
    parser.add_argument('-f', '--dest_folder', type=str, default='media',
                        help='folder for library')
    parser.add_argument('-i', '--skip_imgs',  action='store_true', help='for skip getting images')
    parser.add_argument('-t', '--skip_txt', action='store_true', help='for skip getting books')
    parser.add_argument('-j', '--json_path', type=str, default='media',
                        help='folder for file with info about getting books "books.json"')
    args = parser.parse_args()
    Path(Path.cwd() / args.dest_folder).mkdir(parents=True, exist_ok=True)
    Path(Path.cwd() / args.json_path).mkdir(parents=True, exist_ok=True)
    for page in range(args.start_page, args.end_page + 1):
        url = f'https://tululu.org/l55/{page}/'
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        books_on_page = soup.select('.d_book ')
        for book in books_on_page:
            book_id = book.select_one('a')['href'][2:-1]
            url = f'https://tululu.org/b{book_id}/'
            try:
                book_details = parse_tululu.parse_book_page(parse_tululu.get_response(url))
                book_info = {
                    'title': book_details['title'],
                    'author': book_details['author'],
                }
                if not args.skip_imgs:
                    parse_tululu.download_img(book_details['img'], Path(args.dest_folder, 'images/'))
                    book_info['img_src'] = \
                        f'{args.dest_folder}/images/{unquote(urlsplit(book_details["img"]).path).split("/")[-1]}'
                if not args.skip_txt:
                    parse_tululu.download_txt(book_id, book_details['title'], Path(args.dest_folder, 'books/'))
                    book_info['book_path'] = f'{args.dest_folder}/books/{sanitize_filename(book_details["title"])}.txt'
                book_info['comments'] = book_details['comments']
                book_info['genres'] = book_details['genres']
                books_json = json.dumps(book_info, indent=0, ensure_ascii=False, separators=(', ', ': '))
                with open(Path(args.json_path, 'books.json'), 'a', encoding='utf8') as file:
                    file.write(books_json + ',\n')
                print(url)
            except requests.HTTPError:
                print(f'book with number {book_id} is absent')


if __name__ == '__main__':
    main()
