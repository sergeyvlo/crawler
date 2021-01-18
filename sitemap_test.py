from xml.etree.ElementTree import iterparse
from urllib.error import URLError, HTTPError
from http.client import InvalidURL

from urlopener import Urlopener, openerconfig
from urlopener.request_handlers import UserAgentHandler
from urlopener.idna import idna_encode

from xmlreader import SitemapXML
from urlopener.robots import Robots
import collections

url_base = "http://www.fish.customweb.ru/"
url_base = 'https://bagaznik-darom.ru/'
#url_base = 'https://www.citilink.ru/'
#url_base = 'http://lanatula.ru/'
#url_base =  'https://www.dns-shop.ru/'


# Создание URL открывалки
rec = Urlopener()

rec.add_headers([('Accept', 'text/html'),
                 ('Connection', 'keep-alive'),
                 ('Upgrade-Insecure-Requests', '1')
                ])

# USER-AGENT
agent = UserAgentHandler(openerconfig.agents[2])
rec.add_handler(agent)

url_base = idna_encode(url_base)

# Загрузить robots.txt
parser = Robots()
parser.set_url_ext(url_base)
counter = collections.Counter()
try:
    # Получить USER-AGENT
    parser.site_maps_ext()
    try:
        url_xml_sitemap = parser.maps[openerconfig.USER_AGENT_ROBOTS]
        sitemap_xml = SitemapXML()
        sitemap_xml.sitemap_load(url_xml_sitemap)

        if sitemap_xml.xml_is_load:
            sitemap_xml.make_sitemap_url()
            for url in sitemap_xml.extract_url_from_sitemap():
                #print(rec)
                counter['url'] += 1
                response = rec.urlopen(url)
                if response['redirect'] is not None:
                    print(response['redirect'])

                if response['response'] is not None:
                    print(response['response']['code'], response['response']['url'],
                          response['response']['msg'])

                if response['error'] is not None:
                    print(response['error'])
                print(counter['url'])
    except KeyError:
        print('Такого робота в robots.txt нет.\nУкажите User-agent')
except (UnicodeDecodeError, URLError, HTTPError, InvalidURL, ValueError) as e:
    print('Файл robots.txt отсутствует;', e)




