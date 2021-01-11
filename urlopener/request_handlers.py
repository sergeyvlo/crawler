from urllib.request import BaseHandler, HTTPRedirectHandler, \
    HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm, HTTPCookieProcessor
from http.cookiejar import CookieJar, DefaultCookiePolicy, FileCookieJar, MozillaCookieJar
import collections
from os.path import exists


class RedirectHandler(HTTPRedirectHandler):

    def __init__(self):
        HTTPRedirectHandler.__init__(self)
        self.redirect_hdrs = []
        self.counter = collections.Counter()

    def get_redirect(self):
        if len(self.redirect_hdrs) > 0:
            return self.redirect_hdrs
        else:
            return None

    def clear_redirect(self):
        self.redirect_hdrs = []
        self.counter.clear()

    def redirect_request(self, req, res, code, msg, hdrs, newurl):
        response = {'url': req.get_full_url(), 'headers': res.headers, 'code': code, 'msg': msg, 'new_url': newurl}

        self.redirect_hdrs.append(response)

        nreq = HTTPRedirectHandler.redirect_request(self, req, res, code, msg, hdrs, newurl)

        return nreq

    # Оставил, возможно потребуется
    def http_error_301(self, req, res, code, msg, hdrs):
        # Let parent handle the rest
        return HTTPRedirectHandler.http_error_301(
            self, req, res, code, msg, hdrs)

    # Оставил, возможно потребуется
    def http_error_302(self, req, res, code, msg, hdrs):
        # Let parent handle the rest
        return HTTPRedirectHandler.http_error_302(
            self, req, res, code, msg, hdrs)

    def http_error_303(self, req, res, code, msg, hdrs):
        # Let parent handle the rest
        return HTTPRedirectHandler.http_error_303(
            self, req, res, code, msg, hdrs)

    def http_error_307(self, req, res, code, msg, hdrs):
        #return None
        self.counter['307'] += 1
        if self.counter['307'] <= 1:
            return HTTPRedirectHandler.http_error_307(
                self, req, res, code, msg, hdrs)


class UserAgentHandler(BaseHandler):
    # Handler добавляющий user-agent

    def __init__(self, ua):
        self._ua = ua

    def http_request(self, request):
        request.add_unredirected_header('User-agent', str(self._ua))
        return request

    https_request = http_request


class AuthorizationHandler:

    def __init__(self):
        self.password_mgr = HTTPPasswordMgrWithDefaultRealm()

    def basic_auth(self):
        handler = HTTPBasicAuthHandler(self.password_mgr)
        return handler

    def add_auth_data(self, top_level_url, user, passwd):
        self.password_mgr.add_password(None, top_level_url, user, passwd)


class CookiejarHandler:

    def __init__(self):
        self.cookieJar = None

    def cookiejar(self, policy):
        def_policy = DefaultCookiePolicy(**policy)

        self.cookieJar = CookieJar(def_policy)

        handler = HTTPCookieProcessor(self.cookieJar)
        return handler

    def make_cookies(self, response, request):
        cook = self.cookieJar.make_cookies(response, request)
        return cook

    def clear_cookies(self, domain=None, path=None, name=None):
        self.cookieJar.clear(domain, path, name)


class MozillaCookiejarHandler:
    """Загружает и сохраняет cookies в формате Mozilla"""

    def __init__(self, filename='cookies.txt'):
        self.mozillaCookieJar = None
        self.filename = filename

    def cookiejar(self, policy):
        def_policy = DefaultCookiePolicy(**policy)

        self.mozillaCookieJar = MozillaCookieJar(self.filename, def_policy)
        if exists(self.filename):
            self.mozillaCookieJar.load(self.filename)

        handler = HTTPCookieProcessor(self.mozillaCookieJar)
        return handler

    def save_cookies(self):
        self.mozillaCookieJar.save()

    def make_cookies(self, response, request):
        cook = self.mozillaCookieJar.make_cookies(response, request)
        return cook

    def clear_cookies(self, domain=None, path=None, name=None):
        self.mozillaCookieJar.clear(domain, path, name)