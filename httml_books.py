import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, select_autoescape

from livereload import Server, shell

from more_itertools import chunked

with open('media/books.json', 'r', encoding='utf-8') as file:
    books_json = file.read()
books = json.loads(books_json)
books_col = list(chunked(books, 2))
for book in books:
    book['book_path'] = quote(book['book_path'])



def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')
    rendered_page = template.render(
        books_col=books_col,

    )
    with open('index.html', 'w', encoding="utf-8") as file:
        file.write(rendered_page)


on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
