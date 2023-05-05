import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, select_autoescape

from livereload import Server, shell

from more_itertools import chunked

with open('media/books.json', 'r', encoding='utf-8') as file:
    books_json = file.read()
books = json.loads(books_json)
# books_col = list(chunked(books, 2))
for book in books:
    book['book_path'] = Path(Path.cwd(), quote(book['book_path'])).as_posix()


def on_reload():
    Path(Path.cwd() / 'pages').mkdir(parents=True, exist_ok=True)
    books_pages = list(chunked(books, 20))
    for num_page, books_on_page in enumerate(books_pages):
        books_col = list(chunked(books_on_page, 2))
        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml']))
        template = env.get_template('template.html')
        rendered_page = template.render(
            books_col=books_col,
            prev=Path(Path.cwd(), 'pages', f'index{num_page-1}.html').as_posix() if num_page else Path(Path.cwd(), 'pages', f'index{num_page}.html').as_posix(),
            next=Path(Path.cwd(), 'pages', f'index{num_page+1}.html').as_posix()

        )
        with open(Path('pages', f'index{num_page}.html'), 'w', encoding="utf-8") as file:
            file.write(rendered_page)


on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='pages/index0.html')
