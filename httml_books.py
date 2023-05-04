import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

from livereload import Server, shell




with open('media/books.json', 'r', encoding='utf-8') as file:
    books_json = file.read()
books = json.loads(books_json)



def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')
    rendered_page = template.render(
        books=books
    )
    with open('index.html', 'w', encoding="utf-8") as file:
        file.write(rendered_page)


on_reload()
server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')
