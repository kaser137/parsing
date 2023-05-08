import argparse
import json
from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

NUBER_CARDS_ON_PAGE = 20
NUBER_COLUMNS = 2


def on_reload():
    Path(Path.cwd() / 'pages').mkdir(parents=True, exist_ok=True)
    books_pages = list(chunked(books_details, NUBER_CARDS_ON_PAGE))
    for number_page, books_on_page in enumerate(books_pages, 1):
        books_split_for_columns = list(chunked(books_on_page, NUBER_COLUMNS))
        pages_quantity = len(books_pages)
        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml']))
        template = env.get_template('template.html')
        rendered_page = template.render(
            books_split_for_columns=books_split_for_columns,
            pages_quantity=pages_quantity,
            prev_page=f'../pages/index{number_page - 1}.html',
            next_page=f'../pages/index{number_page + 1}.html',
            current_page=lambda x: f'../pages/index{x}.html',
            number_page=number_page,
        )
        with open(Path('pages', f'index{number_page}.html'), 'w', encoding='utf-8') as file_html:
            file_html.write(rendered_page)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run site with cards and links to the books from "books.json"')
    parser.add_argument('-b', '--books_details_path', nargs='?', default='media/',
                        help='directory where is "books.json"')
    args = parser.parse_args()
    with open(Path(args.books_details_path, 'books.json'), 'r', encoding='utf-8') as books_details_file:
        books_details = json.load(books_details_file)
    for book_details in books_details:
        book_details['book_path'] = f'../{quote(book_details["book_path"])}'
        book_details['img_src'] = f'../{quote(book_details["img_src"])}'
        book_details['genres'] = ' '.join(book_details['genres'])
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(default_filename='pages/index1.html')
