import time
import json
import requests
import urllib.parse
import urllib.request

from tqdm import tqdm
from selenium import webdriver
from bs4 import BeautifulSoup, Tag

MAIN_URL = 'https://tass.ru/'


def get_heading_name(result_set):
    next_links = []

    for tag in result_set:
        if type(tag) != Tag:
            continue

        link = tag.next.contents[0].attrs['href']
        next_links.append(link)

    return next_links


def get_tags(tags_list):
    tags = []
    for _tag in tags_list.contents:
        tags.append(_tag.text)

    tags = ','.join(tags)
    return tags


def get_page_info(link):
    result = {}

    response = urllib.request.urlopen(link)
    soup = BeautifulSoup(response, 'lxml')

    result['article_id'] = link
    result['title'] = soup.find('h1', class_='news-header__title').text
    result['category'] = link.split('/')[3]
    tags_list = soup.find('div', class_='tags__list')
    result['tags'] = get_tags(tags_list)
    result['text'] = soup.find('div', class_='text-block').text

    return result


def parse_tass_news():
    news_parsed = {'catalog': []}

    response = requests.get(MAIN_URL)
    soup = BeautifulSoup(response.text, 'lxml')

    headings = soup.find_all('li', class_='menu-sections-list-item')

    links = get_heading_name(headings)
    links = [links[1], links[4], links[8], links[11]]  # 4 category links (ekonomika, kultura, politika, obschestvo)

    for link in links:

        curr_head = {'catalog': []}
        print(link)
        heading_link = urllib.parse.urljoin(MAIN_URL, link)  # get next link

        driver = webdriver.Firefox()  # open firefox
        driver.get(heading_link)
        for i in range(130):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll down to update tass.ru news
            time.sleep(1)

        html = driver.page_source
        soup = BeautifulSoup(html)

        news = soup.find_all('a', class_='cardWrap_link__2AN_X')  # get data from available news

        if len(news) < 1000:
            print(f'{link} contains only {len(news)} elements')

        for n in tqdm(news[:1000]):
            news_link = urllib.parse.urljoin(MAIN_URL, n.attrs['href'])
            try:
                result_dict = get_page_info(news_link)  # get necessary data
                news_parsed['catalog'].append(result_dict)
                curr_head['catalog'].append(result_dict)
            except:
                continue

        # save file
        with open(f'parsed_news_kuklin_maxim_{link[1:]}.json', 'w') as outfile:
            json.dump(curr_head, outfile, ensure_ascii=False)

    with open('parsed_news_kuklin_maxim.json', 'w') as outfile:
        json.dump(news_parsed, outfile, ensure_ascii=False)


if __name__ == '__main__':
    parse_tass_news()
