from urlopener.robots import Robots
from urlopener.idna import idna_encode
from urllib import parse
from urllib.error import URLError, HTTPError
from http.client import InvalidURL


url_base = "https://bagaznik-darom.ru/"
url_base = "http://www.fish.customweb.ru/"
#url_base = "https://www.dns-shop.ru/"
#url_base = 'https://www.onlinetrade.ru/'
#url_base = 'https://юзерагент.рф/'
#url_base = 'http://lanatula.ru/'

USER_AGENT = '*'

PARTS = [
    '/',
    '/admin/?menu=catalog',
    'http://www.fish.customweb.ru/admin/',
    '/docs/',
    '/preorder/',
    '/catalog/boks_lux_irbis_175_seriy_matoviy_450l_s_dvustor_otkr_1750h850h400_art_790951',
    'boks_lux_irbis_175_seriy_matoviy_450l_s_dvustor_otkr_1750h850h400_art_790951',
    '/avtoboksi/?set=page',
    '*?',
    '*?*'
]

url_base = idna_encode(url_base)
parser = Robots()
parser.set_url_ext(url_base)

try:
    parser.site_maps_ext()
except (UnicodeDecodeError, URLError, HTTPError, InvalidURL, ValueError) as e:
    print('Файл robots.txt отсутствует;', e)

print(parser.maps)
try:
    parser.read()
except (UnicodeDecodeError, URLError, HTTPError, InvalidURL, ValueError) as e:
    print('Файл robots.txt отсутствует;', e)


for path in PARTS:
    print('{!r:>6} : {}'.format(
        parser.can_fetch(USER_AGENT, path), path
    ))

    url = parse.urljoin(url_base, path)

    print('{!r:>6} : {}'.format(
        parser.can_fetch(USER_AGENT, url), url
    ))
    print('-' * 25)

# Sets the time the robots.txt file was last fetched to the current time.
print('\nметод modified()')
print(parser.modified())

print('\nметод crawl_delay() New in version 3.6')
try:
    print(parser.crawl_delay(USER_AGENT))
except AttributeError:
    print('Нет такого')

print('\nметод request_rate() New in version 3.6')
try:
    print(parser.request_rate(USER_AGENT))
except AttributeError:
    print('Нет такого')

# Реализовывать отдельно
print('\nметод site_maps() New in version 3.8')
try:
    print(parser.site_maps())
except AttributeError:
    print('Нет такого')

print(parser)