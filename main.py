import requests
from pathlib import Path

Path("./books").mkdir(parents=True, exist_ok=True)


def check_for_redirect(r):
    if r.history:
        raise requests.HTTPError


url_start = 'https://tululu.org/txt.php?id=32168'
for i in range(1, 11):
    url = f'https://tululu.org/txt.php?id={i}'
    r = requests.get(url)
    r.raise_for_status()
    try:
        check_for_redirect(r)
        with open(f'books/id{i}.txt', 'w') as file:
            file.write(r.text.replace('\xa0', ' '))
    except requests.HTTPError:
        continue
