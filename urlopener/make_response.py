from urlopener import openerconfig


class MakeResponse:

    def __init__(self, encoding=openerconfig.ENCODING):
        self.encoding = encoding
        self.mime_type = None

    def make_response(self, response, url):
        """Метод выдает запрос"""
        # Получить кодировку, mimetype, иначе UTF-8
        self.__define_mime_encode(response)

        if self.mime_type in openerconfig.MIME_TYPES:
            data = response.read().decode(self.encoding)
        else:
            data = None

        response = {'url': url, 'headers': response.headers, 'code': response.getcode(),
                    'msg': response.msg, 'new_url': response.geturl(), 'data': data}

        return response

    def make_redirect(self, redirect_handler):
        """Метод выдает редирект"""
        redirect = redirect_handler.get_redirect()
        redirect_handler.clear_redirect()
        return redirect

    def make_cookies(self, cookie_handler, response, request):
        """Метод выдает cookie"""
        cookie = cookie_handler.make_cookies(response, request)
        return cookie

    def make_error(self, url, code, msg):
        """Метод выдает ошибку"""
        error = {'url': url, 'code':code, 'msg': msg}
        return error

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