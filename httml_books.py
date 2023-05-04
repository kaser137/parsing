import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml']))

template = env.get_template('template.html')
with open('media/books.json', 'r', encoding='utf-8') as file:
    books_json = file.read()
books = json.loads(books_json)
rendered_page = template.render(
    books=books
)

with open('index.html', 'w', encoding="utf-8") as file:
    file.write(rendered_page)