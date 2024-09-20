from http import HTTPStatus
import os
import string
import requests
from bs4 import BeautifulSoup

URL = 'https://www.nature.com/nature/articles'
URL_HOME = 'https://www.nature.com'

params = {
    'searchType': 'journalSearch',
    'sort': 'PubDate',
    'year': '2020',
    'page': '1'
}


def main():
    pages_num = int(input())
    article_type = input()
    articles = []

    for page_num in range(1, pages_num + 1):
        params['page'] = str(page_num)
        response = requests.get(URL, params=params)
        if response.status_code != HTTPStatus.OK:
            print(f'\nThe URL returned {response.status_code}!')
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        articles.append(soup.find_all('article'))

    for i, page in enumerate(articles):
        os.mkdir(f'Page_{i + 1}')
        for article in page:
            if article.find('span', {'data-test': 'article.type'}).text == article_type:
                article_link = article.find('a', {'data-track-action': 'view article'}).get('href')
                response_2 = requests.get(URL_HOME + article_link)
                if response_2.status_code != HTTPStatus.OK:
                    print(f'\nThe URL returned {response_2.status_code}!')
                    return
                soup_2 = BeautifulSoup(response_2.text, 'html.parser')
                article_title = ''.join(char for char in soup_2.title.text if char not in string.punctuation)
                article_title = article_title.strip().replace(' ', '_')
                file_name = article_title + '.txt'
                article_content = soup_2.find('p', class_='article__teaser').text.strip()

                with open(f'Page_{i + 1}/' + file_name, 'wb') as file:
                    file.write(article_content.encode('utf-8'))


if __name__ == '__main__':
    main()
