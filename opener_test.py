from urlopener import Urlopener, openerconfig
from urlopener.request_handlers import AuthorizationHandler, UserAgentHandler
from urlopener.idna import idna_encode
from urlopener.robots import Robots
from urllib.error import URLError, HTTPError
from http.client import InvalidURL


# from urlopener import *
# import urlopener.openerconfig as openerconfig

if __name__ == '__main__':

    urls = (
        'https://docs.python.org/3.8/library/tkinter.html',
        'https://bagaznik-darom.ru/',
        'http://www.fish.customweb.ru/robots.txt',
        'http://www.fish.customweb.ru/admin/',
        'http://fish.customweb.ru/',
        #'https://www.dns-shop.ru/robots.txt',
        'http://lanatula.ru/about/',
        'http://www.lanatula.ru/about/',
        'http://lanatula.ru/about1/',
        'http://192.168.1.93/phpinfo.php',
        'http://кто.рф/',
        #'https://yandex.ru/search/?text=idna что это&lr=15',
        'https://docs.python.org/3.8/library/tkinter1.html',
        'http://www.customweb.ru/images/flags/ad/ad.gif',
        'http://www.customweb.ru/images/flags/ad/metadata.json',
        'http://lana:tula.ru/about1/',
        'http1://lanatula.ru/about1/',
        'http://demo.customweb.ru/',
        'http://demo.customweb.ru/we/wecannot/',
        'http://demo2.customweb.ru/',
        'http://demo20.customweb.ru/',
        'https://www.dns-shop.ru/product/f30ac0bcc3913330/blok-pitania-sven-350w-pu-350an/ddd/',
        'https://www.dns-shop.ru/',
        'http://fish.customweb.ru/',
        'https://юзерагент.рф/',
        'https://русские-домены.рф/'
    )

    rec = Urlopener()

    # Базовая идентификация
    auth_handler = AuthorizationHandler()
    for auth in openerconfig.BASIC_AUTH:
        auth_handler.add_auth_data(*auth)
    rec.add_handler(auth_handler.basic_auth())

    # USER-AGENT
    agent = UserAgentHandler(openerconfig.agents[2])
    rec.add_handler(agent)

    bad_robot = None

    for url in urls:
        # Для открытия международных доменов
        url = idna_encode(url)

        # Использовать robots.txt
        if openerconfig.USE_ROBOTS:
            parser = Robots()
            parser.make_robots(url)

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
            response = rec.urlopen(url)
        else:
            bad_robot = ('URL закрыт', url)


        if response['redirect'] is not None:
            print(response['redirect'])
            response['redirect'] = None
        if response['response'] is not None:
            print(response['response']['code'], response['response']['url'], response['response']['msg'])
            response['response'] = None
        if response['error'] is not None:
            print(response['error'])
            response['error'] = None
        if bad_robot is not None:
            print(bad_robot)
            bad_robot = None

        print('----------')
