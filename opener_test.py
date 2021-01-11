from urlopener import Urlopener, openerconfig
from urlopener.request_handlers import AuthorizationHandler, UserAgentHandler, CookiejarHandler
from urlopener.idna import idna_encode
from urlopener.robots import Robots

from urllib.error import URLError, HTTPError
from http.client import InvalidURL
from http.cookiejar import CookieJar, DefaultCookiePolicy


# from urlopener import *
# import urlopener.openerconfig as openerconfig

if __name__ == '__main__':

    urls = (
        'https://www.citilink.ru/catalog/computers_and_notebooks/parts/videocards/352141/',
        'https://www.onlinetrade.ru/catalogue/videokarty-c338/',
        #'https://www.dns-shop.ru/robots.txt',
        'https://www.dns-shop.ru/category.xml',
        'https://www.dns-shop.ru/catalog/212b482fcdc66369/remont-i-dekor/',
        'https://www.dns-shop.ru/catalog/17a88ba616404e77/avtotovary/',
        'https://bagaznik-darom.ru/',
        'http://www.fish.customweb.ru/robots.txt',
        'http://www.fish.customweb.ru/',
        'http://fish.customweb.ru/',
        'http://lanatula.ru/',
        'http://lanatula.ru/admin/',
        'http://www.lanatula.ru/about/',
        'http://lanatula.ru/about1/',
        'http://192.168.1.93/phpinfo.php',
        'http://кто.рф/',
        #'https://yandex.ru/search/?text=idna что это&lr=15',
        'https://docs.python.org/3.8/library/tkinter1.html',
        'https://docs.python.org/3.8/library/tkinter.html',
        'http://www.customweb.ru/images/flags/ad/ad.gif',
        'http://www.customweb.ru/images/flags/ad/metadata.json',
        'http://lana:tula.ru/about1/',
        'http1://lanatula.ru/about1/',
        'http://demo.customweb.ru/',
        'http://demo.customweb.ru/we/wecannot/',
        'http://demo2.customweb.ru/',
        'http://demo20.customweb.ru/',
        #'https://www.dns-shop.ru/product/f30ac0bcc3913330/blok-pitania-sven-350w-pu-350an/ddd/',
        'http://fish.customweb.ru/admin/',
        #'https://юзерагент.рф/',
        #'https://русские-домены.рф/'
    )

    # Создание URL открывалки
    rec = Urlopener()

    rec.add_headers([('Accept', 'text/html'),
                     ('Connection', 'keep-alive'),
                     ('Upgrade-Insecure-Requests', '1')
                     ])

    # Базовая идентификация
    auth_handler = AuthorizationHandler()
    for auth in openerconfig.BASIC_AUTH:
        auth_handler.add_auth_data(*auth)
    rec.add_handler(auth_handler.basic_auth())

    # USER-AGENT
    agent = UserAgentHandler(openerconfig.agents[2])
    rec.add_handler(agent)

    # cookies
    if openerconfig.COOKIES:
        policy = {'rfc2965': True, 'strict_ns_domain': DefaultCookiePolicy.DomainStrict}
        rec.add_cookie_handler(policy=policy, filename='cookies.txt')

    bad_robot = None

    for url in urls:
        # Для открытия международных доменов
        url = idna_encode(url)

        # Использовать robots.txt
        if openerconfig.USE_ROBOTS:
            parser = Robots()
            parser.set_url_ext(url)

            # Возможно прочитать robots.txt
            try:
                parser.read()
            # Неудается прочитать robots.txt
            except (UnicodeDecodeError, URLError, HTTPError, InvalidURL, ValueError):
                pass

        # Проверка доступа к URL в robots.txt
        if openerconfig.USE_ROBOTS:
            flag_url = parser.can_fetch(openerconfig.USER_AGENT, url)
        else:
            flag_url = True

        if flag_url:
            response = rec.urlopen(url)     # Открыть URL
        else:
            bad_robot = ('URL закрыт', url)

        if openerconfig.COOKIES:
            #print(rec.cookie_handler.make_cookies(response, rec))
            pass

        if openerconfig.COOKIES:
            print(response['cookie'])

        #print(response)

        if response['redirect'] is not None:
            print(response['redirect'])

        if response['response'] is not None:
            print(response['response']['code'], response['response']['url'], response['response']['msg'])

        if response['error'] is not None:
            print(response['error'])

        if bad_robot is not None:
            print(bad_robot)
            bad_robot = None


        response = None
        print('----------')

    if openerconfig.COOKIES:
        rec.cookie_handler.save_cookies()