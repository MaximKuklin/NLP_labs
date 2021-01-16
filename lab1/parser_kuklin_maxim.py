import requests
from bs4 import BeautifulSoup, Tag
import urllib.parse
from selenium import webdriver
import time


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
    for _tag in tags_list.content:
         tags.append(_tag.text)

    tags = ','.join(tags)
    return tags

def get_page_info(link):
    result = {}

    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')

    result['article_id'] = link
    result['title'] = soup.find('h1', class_='news-header__title').text
    result['category'] = link.split('/')[3]
    tags_list = soup.find('div', class_='tags__list')
    result['tags'] = get_tags(tags_list)
    result['text'] = soup.find('div', class_='text-block').text

    return result

main_url = 'https://tass.ru/'
response = requests.get(main_url)
soup = BeautifulSoup(response.text, 'lxml')

headings = soup.find_all('li', class_='menu-sections-list-item')

links = get_heading_name(headings)


news_parsed = {'catalog': []}

for link in links:
    heading_link = urllib.parse.urljoin(main_url, link)

    driver = webdriver.Firefox()
    driver.get(heading_link)
    # for i in range(125):
    for i in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.01)

    html = driver.page_source
    soup = BeautifulSoup(html)

    news = soup.find_all('a', class_='cardWrap_link__2AN_X')

    for n in news:
        news_link = urllib.parse.urljoin(main_url, n.attrs['href'])
        result_dict = get_page_info(news_link)
        news_parsed['catalog'].append(result_dict)
