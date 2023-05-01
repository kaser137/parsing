# Парсер книг

Эта программа скачивает книги и обложки с сайта [БОЛЬШАЯ БЕСПЛАТНАЯ БИБЛИОТЕКА](https://tululu.org/)

## Подготовка

- Скачайте код
- Установите зависимости командой:
```commandline
pip install -r requirements.txt
``` 

## Администрирование parse_tululu.py

- Запустите программу командой
```commandline
python parse_tululu.py
```
- По умолчанию программа скачивает книги с 1 по 10.
- Вы можете указать диапазон книг для скачивания:
```commandline
python parse_tululu.py 115 213
```
- Скачанные книги и обложки будут сохранены в папках "books" и "images", соответственно.
- Если папки отсутствуют, программа их создаст.
- Файлы в этих папках могут быть перезаписаны.

## Администрирование parse_tululu_category.py
- Запустите программу командой
```commandline
python parse_tululu_category.py
```

- По умолчанию программа скачивает книги со всех страниц с 1 по 701.
- Вы можете указать диапазон книг для скачивания, например:
```commandline
python parse_tululu_category.py --start_page [or -s] 33
```
```commandline
python parse_tululu_category.py --start_page [or -s] 25 --end_page [or -e] 50
```
- По умолчанию скачанные книги и обложки будут сохранены в папках "media/books", "media/images". Если папки отсутствуют, скрипт их создаст.
- Вы можете указать папки, например:
```commandline
python parse_tululu_category.py --dest_folder [or -f]'Папка для книг и обложек' --json_path [or -j]'Папка для файла с информацией о книгах' 
```

Вы можете выключить загрузку книг или обложек, например:
```commandline
python parse_tululu_category.py --skip_txt [or -t] --skip_imgs [or -i]
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
 