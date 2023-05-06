import json
from pathlib import Path
from urllib.parse import quote
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def main():
    with open('media/books.json', 'r', encoding='utf-8') as file:
        books_json = file.read()
    books = json.loads(books_json)

    for book in books:
        book['book_path'] = f'../{quote(book["book_path"])}'
        book['genres'] = ' '.join(book['genres'])

    def on_reload():
        Path(Path.cwd() / 'pages').mkdir(parents=True, exist_ok=True)
        books_pages = list(chunked(books, 20))

        for num_page, books_on_page in enumerate(books_pages, 1):
            books_split_for_columns = list(chunked(books_on_page, 2))
            pages_quantity = len(books_pages)
            env = Environment(
                loader=FileSystemLoader('.'),
                autoescape=select_autoescape(['html', 'xml']))
            template = env.get_template('template.html')
            rendered_page = template.render(
                books_split_for_columns=books_split_for_columns,
                pages_quantity=pages_quantity,
                prev=f'../pages/index{num_page - 1}.html',
                next=f'../pages/index{num_page + 1}.html',
                current=lambda x: f'../pages/index{x}.html',
                num_page=num_page,
            )
            with open(Path('pages', f'index{num_page}.html'), 'w', encoding="utf-8") as file:
                file.write(rendered_page)

    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(default_filename='pages/index1.html')


if __name__ == '__main__':
    main()
