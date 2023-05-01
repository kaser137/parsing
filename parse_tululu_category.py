import requests
import argparse
import json
import sys
from bs4 import BeautifulSoup
from pathlib import Path
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
    books_specifics = []
    for page in range(args.start_page, args.end_page + 1):
        url = f'https://tululu.org/l55/{page}/'
        try:
            response = parse_tululu.get_response(url)
            soup = BeautifulSoup(response.text, 'lxml')
            books_on_page = soup.select('.d_book ')
            for book in books_on_page:
                book_id = book.select_one('a')['href'][2:-1]
                url = f'https://tululu.org/b{book_id}/'
                try:
                    book_details = parse_tululu.parse_book_page(parse_tululu.get_response(url))
                    book_specifics = {
                        'title': book_details['title'],
                        'author': book_details['author'],
                    }
                    if not args.skip_imgs:
                        img_src = parse_tululu.download_img(book_details['img'], Path(args.dest_folder, 'images/'))
                        book_specifics['img_src'] = img_src
                    if not args.skip_txt:
                        book_path = parse_tululu.download_txt(book_id, book_details['title'],
                                                              Path(args.dest_folder, 'books/'))
                        book_specifics['book_path'] = book_path
                    book_specifics['comments'] = book_details['comments']
                    book_specifics['genres'] = book_details['genres']
                    books_specifics.append(book_specifics)
                except requests.HTTPError:
                    print(f'book with number {book_id} is absent')
        except requests.HTTPError as err:
            print(f'during request has occurred such error: {err}', file=sys.stderr)
    with open(Path(args.json_path, 'books.json'), 'w', encoding='utf8') as file:
        json.dump(books_specifics, file, indent=0, ensure_ascii=False)


if __name__ == '__main__':
    main()
