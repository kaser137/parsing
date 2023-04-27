import requests
# import lxml
from bs4 import BeautifulSoup


def main():
    url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
    r = requests.get(url)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, 'lxml')
    print(soup.find('h1', class_="entry-title").text, '\n')
    print(soup.find('img', class_='attachment-post-image')['src'], '\n')
    print(soup.find(class_="entry-content").text)


if __name__=='__main__':
    main()