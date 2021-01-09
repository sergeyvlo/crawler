from urlopener import Urlopener, openerconfig


if __name__ == '__main__':
    url = 'http://192.168.1.93/test_headers.php'
    url = 'https://www.dns-shop.ru/'
    url = 'https://bagaznik-darom.ru/robots.txt'

    rec = Urlopener()
    #rec.add_headers([('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
    #                     ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'),
    #                 ('Connection', 'keep-alive'),
    #                 ('Upgrade-Insecure-Requests', '1'),
    #                 ('Accept-Language', 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3')
    #                 ])
    response = rec.urlopen(url)

    #if response['response'] is not None:
    #    print(response['response']['data'])

    if response['redirect'] is not None:
        print(response['redirect'])
        response['redirect'] = None
    if response['response'] is not None:
        print(response['response']['code'], response['response']['url'], response['response']['msg'])
        response['response'] = None
    if response['error'] is not None:
        print(response['error'])
        response['error'] = None