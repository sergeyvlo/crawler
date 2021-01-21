from http.cookiejar import DefaultCookiePolicy
from urllib.error import URLError, HTTPError
from http.client import InvalidURL

from urlopener import Urlopener, openerconfig
from urlopener import MakeResponse


if __name__ == '__main__':
    url = 'http://192.168.1.93/test_headers.php'
    #url = 'https://www.dns-shop.ru/'
    #url = 'https://bagaznik-darom.ru/robots.txt'

    rec = Urlopener()
    make_response = MakeResponse()

    rec.add_headers([('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
                         ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'),
                     #('Connection', 'keep-alive'),
                     #('Upgrade-Insecure-Requests', '1'),
                     #('Accept-Language', 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3')
                     ])

    # cookies
    if openerconfig.COOKIES:
        policy = {'rfc2965': True, 'strict_ns_domain': DefaultCookiePolicy.DomainStrict}
        rec.add_cookie_handler(policy=policy, filename='cookies.txt')

    #response = rec.urlopen(url)
    response = {'response': None, 'redirect': None, 'error': None}
    try:
        rec.urlopen(url)  # Открыть URL
        response['response'] = make_response.make_response(rec.response, url)
        response['redirect'] = make_response.make_redirect(rec.redirect_handler)
        if openerconfig.COOKIES:
            cookie = make_response.make_cookies(rec.cookie_handler, rec.response, rec.request)

    except HTTPError as e:
        response['error'] = make_response.make_error(url, e.code, str(e))

    except URLError as e:  # Ошибки URL
        response['error'] = make_response.make_error(url, e.errno, e.reason)

    except InvalidURL as e:
        response['error'] = make_response.make_error(url, -1, str(e))


    if response['redirect'] is not None:
        print(response['redirect'])
        response['redirect'] = None
    if response['response'] is not None:
        print(response['response']['data'])
        print(response['response']['code'], response['response']['url'], response['response']['msg'])
        response['response'] = None
    if response['error'] is not None:
        print(response['error'])
        response['error'] = None

    if openerconfig.COOKIES:
        print(cookie)
        rec.cookie_handler.save_cookies()