from urlopener import Urlopener, openerconfig
from urlopener.request_handlers import AuthorizationHandler, UserAgentHandler


# from urlopener import *
# import urlopener.openerconfig as openerconfig

if __name__ == '__main__':

    urls = (
        'https://docs.python.org/3.8/library/tkinter.html',
        'https://bagaznik-darom.ru/',
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
       # 'https://www.dns-shop.ru/product/f30ac0bcc3913330/blok-pitania-sven-350w-pu-350an/1'
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

    for url in urls:
        response = rec.urlopen(url)

        if response['redirect'] is not None:
            print(response['redirect'])
        if response['response'] is not None:
            print(response['response']['code'], response['response']['url'], response['response']['msg'])
        if response['error'] is not None:
            print(response['error'])

        print('/n----------')
