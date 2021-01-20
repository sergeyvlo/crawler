from urllib.parse import urlsplit, urlunsplit
from urllib.error import URLError, HTTPError
from http.client import InvalidURL


def get_base_url(url):
    parts = list(urlsplit(url))
    parts[2] = ''
    parts[3] = ''
    parts[4] = ''
    url = urlunsplit(parts)
    return url


import reprlib
reprlib.Repr.maxlong = 80


class ListInstance:

    def __str__(self):
        return '<Экземпляр of %s(%s), адрес %s:\n%s>' % (
                self.__class__.__name__,      # Имя моего класса
                self.__suppers(),             # Мои суперклассы
                id(self),                     # Адрес экземпляра
                self.__attrnames())           # Список name=value

    def __attrnames(self):
        result = ''
        for attr in sorted(self.__dict__):    # Словарь атрибутов
            result += '\tатрибут: %s=%s\n' % (attr, self.__dict__[attr])
        return result

    def __suppers(self):
        names = []
        for super in self.__class__.__bases__:
            names.append(super.__name__)
            return ', '.join(names)


def print_response(response):
    if response['redirect'] is not None:
        print(response['redirect'])
        response['redirect'] = None
    if response['response'] is not None:
        print(response['response']['code'], response['response']['url'], response['response']['msg'])
        response['response'] = None
    if response['error'] is not None:
        print(response['error'])
        response['error'] = None