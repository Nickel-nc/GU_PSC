# ## Методы сбора и обработки данных из сети Интернет

# ### Парсинг HTML XPath

# Приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru.
# Для парсинга использован xpath. Структура данных содержит:
# * название источника,
# * наименование новости,
# * ссылку на новость,
# * дата публикации

from pprint import pprint
from lxml import html
import requests
from pprint import pprint
import pandas as pd
from datetime import datetime


link_lenta = 'https://lenta.ru'
link_mail = 'https://mail.ru'
headers = {'User-agent': 
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
           AppleWebKit/537.36 (KHTML, like Gecko) \
           Chrome/77.0.3865.90 Safari/537.36'}


def get_news_from_lenta_ru(link, headers=headers):
    req = requests.get(link, headers=headers).text
    root = html.fromstring(req)   
    
    # time
    time = root.xpath(
        '//time[@class="g-time"]/text()'
    )
    raw_news = root.xpath(
        '//time[@class="g-time"]/../text()'
    )
    hrefs = root.xpath(
        '//time[@class="g-time"]/../@href'
    )
    
    # news
    news = []
    for item in raw_news:
        r = item.replace('\xa0',' ')
        news.append(r)
    
    # href
    href = []
    for item in hrefs:
        href.append(link + item)
    
    #site
    site = [link] * len(news)
        
    return list(zip(time, news, href, site))


def get_news_from_mail_ru(link, headers=headers):
    req = requests.get(link, headers=headers).text
    root = html.fromstring(req)
    
    # News
    keys= [0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16] # List of №-news scrapped
    n = root.xpath(
        '//div[contains(@class, "news-item")]//a[last()]//text()'
    )
    news = ([n[i] for i in keys]) # Scip extended text block from main_news
    
    # href
    href = root.xpath(
        '//div[contains(@class, "news-item")]//a[last()]//@href'
    )
    
    # time
    t = datetime.now()
    now = str(t.hour) + ':' + str(t.minute)    
    time = [now] * len(news)
    
    # site
    site = [link] * len(news) 
    
    return list(zip(time, news, href, site))


def make_df(data):
    cols = [
        'Time',
        'News',
        'href',
        'Resource'
    ]
     
    return pd.DataFrame(data, columns=cols)


df_lenta = make_df(get_news_from_lenta_ru(link_lenta))
df_mail = make_df(get_news_from_mail_ru(link_mail))
