from urllib.request import build_opener, Request
from urllib.error import URLError, HTTPError
from http.client import InvalidURL

from .request_handlers import RedirectHandler, CookiejarHandler, MozillaCookiejarHandler
from urlopener import openerconfig


class Urlopener:

    def __init__(self, encoding=openerconfig.ENCODING, timeout=None):
        self.timeout = timeout
        self.encoding = encoding

        self.mime_type = None
        self.res = None

        self.redirect_handler = RedirectHandler()
        self.cookie_handler = None

        # Создать открывалку
        self.opener = build_opener(self.redirect_handler)

        # self.opener.add_handler(self.redirect_handler)

    def add_handler(self, handler):
        """Метод добавляет обработчик"""
        self.opener.add_handler(handler)

    def add_cookie_handler(self, policy={}, filename='cookies.txt'):
        """Метод добавляет обработчик Cookie"""
        self.cookie_handler = MozillaCookiejarHandler(filename)
        self.opener.add_handler(self.cookie_handler.cookiejar(policy))

    def add_headers(self, headers):
        """Метод добавляет заголовки в запрос"""
        self.opener.addheaders = headers

    def urlopen(self, url):
        """Открывает URL"""
        self.redirect_handler.clear_redirect()
        response = {'response': None, 'redirect': None, 'error': None, 'cookie': None}

        req = Request(url)

        try:
            self.res = self.opener.open(req, timeout=self.timeout)
            response['response'], response['redirect'] = self.make_response(self.res, url)
            if self.cookie_handler is not None:
                response['cookie'] = self.cookie_handler.make_cookies(self.res, req)

        except HTTPError as e:
            response['error'] = {'url': url, 'code': e.code, 'msg': str(e)}
            #if self.res is not None:
            #    r, response['redirect'] = self.make_response(self.res, url)

        except URLError as e:  # Ошибки URL
            response['error'] = {'url': url, 'code': e.errno, 'msg': e.reason}

        except InvalidURL as e:
            response['error'] = {'url': url, 'code': -1, 'msg': str(e)}

        return response

    def make_response(self, res, url):
        """Метод выдает ответ"""
        # Получить кодировку, mimetype, иначе UTF-8
        self.__define_mime_encode(res)

        if self.mime_type in openerconfig.MIME_TYPES:
            data = res.read().decode(self.encoding)
        else:
            data = None

        response = {'url': url, 'headers': res.headers, 'code': res.getcode(),
                    'msg': res.msg, 'new_url': res.geturl(), 'data': data}

        redirect = self.redirect_handler.get_redirect()

        self.redirect_handler.clear_redirect()

        return response, redirect

    def __define_mime_encode(self, res):
        """
        Метод определяет кодировку страницы.
        Если не указана кодировка, то используется openerconfig.ENCODING
        """
        content_type = res.headers['Content-Type'].split(';')
        self.mime_type = content_type[0]

        if len(content_type) > 1:
            self.encoding = content_type[1].split('=')[1]
        else:
            self.encoding = openerconfig.ENCODING
