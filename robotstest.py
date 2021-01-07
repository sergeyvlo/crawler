from urllib import robotparser
from urllib import parse

from urlopener.idna import idna_encode


#url_base = "https://bagaznik-darom.ru/"
url_base = "http://www.fish.customweb.ru/"
#url_base = "https://www.dns-shop.ru/"
#url_base = 'https://www.onlinetrade.ru/'
#url_base = 'https://юзерагент.рф/'

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

parser = robotparser.RobotFileParser()
parser.set_url(parse.urljoin(idna_encode(url_base), 'robots.txt'))
parser.read()


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