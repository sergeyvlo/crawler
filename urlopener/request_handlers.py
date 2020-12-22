from urllib.request import BaseHandler, HTTPRedirectHandler, \
    HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm


class RedirectHandler(HTTPRedirectHandler):

    def __init__(self):
        self.redirect_hdrs = []

    def get_redirect(self):
        if len(self.redirect_hdrs) > 0:
            return self.redirect_hdrs
        else:
            return None

    def clear_redirect(self):
        self.redirect_hdrs = []

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
