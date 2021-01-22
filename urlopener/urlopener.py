from urllib.request import build_opener, Request

from .request_handlers import RedirectHandler, CookiejarHandler, MozillaCookiejarHandler
from urlopener import openerconfig


class Urlopener:

    def __init__(self, timeout=None):
        self.timeout = timeout
        # Ответ
        self.response = None
        # Запрос
        self.request = None

        # Обработчик редиректов
        self.redirect_handler = RedirectHandler()
        # Обработчик cookie файлов
        self.cookie_handler = None

        # Создать открывалку
        self.opener = build_opener(self.redirect_handler)

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
        # Очистить предыдущие редиректы
        self.redirect_handler.clear_redirect()

        self.request = Request(url)
        self.response = self.opener.open(self.request, timeout=self.timeout)
