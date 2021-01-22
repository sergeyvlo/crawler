from xml.etree.ElementTree import iterparse
from urllib.error import URLError, HTTPError
from http.client import InvalidURL
from http.cookiejar import DefaultCookiePolicy

from urlopener import Urlopener, openerconfig, MakeResponse
from urlopener.request_handlers import UserAgentHandler
from urlopener.idna import idna_encode

from sitemapxml import SitemapXML
from urlopener.robots import Robots
import collections
from urlopener.utils import print_response

url_base = "http://www.fish.customweb.ru/"
#url_base = 'https://bagaznik-darom.ru/'
#url_base = 'https://www.citilink.ru/'
#url_base = 'http://lanatula.ru/'
#url_base =  'https://www.dns-shop.ru/'
#url_base = 'http://кто.рф/'


# Создание URL открывалки
rec = Urlopener()
make_response = MakeResponse()

rec.add_headers([('Accept', 'text/html'),
                 ('Connection', 'keep-alive'),
                 ('Upgrade-Insecure-Requests', '1')
                ])

# USER-AGENT
agent = UserAgentHandler(openerconfig.agents[2])
rec.add_handler(agent)

# cookies
if openerconfig.COOKIES:
    policy = {'rfc2965': True, 'strict_ns_domain': DefaultCookiePolicy.DomainStrict}
    rec.add_cookie_handler(policy=policy, filename='cookies.txt')

# Загрузить robots.txt
parser = Robots()
url_base = idna_encode(url_base)
parser.set_url_ext(url_base)

counter = collections.Counter()

try:
    rec.urlopen(parser.url_robots)  # Открыть URL
    response = make_response.make_response(rec.response, parser.url_robots)
    redirect = make_response.make_redirect(rec.redirect_handler)

    # Файл robots.txt загружен
    if redirect is None:
        parser.site_maps_ext(response['data'])
        sitemap_xml = SitemapXML(rec)
        url_xml_sitemap = parser.maps[openerconfig.USER_AGENT_ROBOTS]

        # Загрузить sitemap.xml
        #sitemap_xml.sitemap_load(url_xml_sitemap)
        sitemap_xml.xml_load(url_xml_sitemap)

        # Удалось загрузить sitemap.xml
        if sitemap_xml.xml_is_load:
            #Формирует список URL-ов файлов XML sitemap
            sitemap_xml.make_sitemap_url()

            # Обход файла/файлов xml с картой сайта
            for url in sitemap_xml.extract_url_from_sitemap():
                response = {'response': None, 'redirect': None, 'error': None}
                counter['url'] += 1

                # Открыть URL
                try:
                    url = idna_encode(url)
                    rec.urlopen(url)
                    response['response'] = make_response.make_response(rec.response, url)
                    response['redirect'] = make_response.make_redirect(rec.redirect_handler)
                except HTTPError as e:
                    response['error'] = make_response.make_error(url, e.code, str(e))
                except URLError as e:  # Ошибки URL
                    response['error'] = make_response.make_error(url, e.errno, e.reason)
                except InvalidURL as e:
                    response['error'] = make_response.make_error(url, -1, str(e))

                print_response(response)

                print(counter['url'])
    else:
        print('Файл robots.txt не найден:', parser.url_robots, redirect[0]['code'], redirect[0]['msg'])

except (HTTPError, URLError, InvalidURL) as e:
    print('Файл robots.txt не найден:', parser.url_robots, str(e))
except KeyError:
        print('Такого робота в robots.txt нет.\nУкажите User-agent')