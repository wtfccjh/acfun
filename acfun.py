import requests
from bs4 import BeautifulSoup
import codecs

target_url = 'http://www.acfun.tv/v/list110/index_1.htm'
True_url = 'http://www.acfun.tv/v/list110/'


def download_page(url):
    return requests.get(url).content


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    article_list_soup = soup.find('div', attrs={'class': "block"})
    article_name_list = []
    for article_item in article_list_soup.find_all('div', attrs={'class': 'item'}):
        article_name = article_item.find('a', attrs={'class': 'title'}).getText()
        article_name_list.append(article_name)
    next_page = soup.find('div', attrs={'class': 'area-pager'})
    a = next_page.find_all('a', attrs={'class': 'pager'})
    if a[-1]:
        return article_name_list, True_url + a[-1]['href']
    return article_name_list, None


def main():
    url = target_url
    with codecs.open('article', 'wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            article, url = parse_html(html)
            fp.write(u'{article}\n'.format(article='\n'.join(article)))

if __name__ == '__main__':
    main()