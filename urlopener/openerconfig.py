"""
Конфигфайл для пакета oprner.
Если использовать как пакет, правится напрямую.
Если использвать в проекте можно изменить в контенте приложения
(ноывые значения взять из ini файла , базы данных и т.д.)
"""
# USER-AGENT
from urlopener import useragent

"""Выбираться будет из базы или ini файла"""
agents = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ',
          '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
          'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0']

USER_AGENT = useragent.opener_agent()
#USER_AGENT = agents[0]

# Кодировка по умолчанию
ENCODING = 'UTF-8'

# Прокси сервер

# MIME типы, для которых сохраняются текстовые данные
MIME_TYPES = ('text/html', 'text/plain', 'application/json')

# Базовая Идентификация
BASIC_AUTH = (('http://demo.customweb.ru/', 'admin', '12345'),
             ('http://demo2.customweb.ru', 'admin', 'admin'))



