"""
Обрабатывает robots.txt
Базовый url для интернациональных доменов должен декодироваться
в idn заранее
"""
from urllib.robotparser import RobotFileParser
from urllib.request import urlopen
from urllib import parse
from urllib.error import URLError, HTTPError
from http.client import InvalidURL

from .utils import get_base_url

class Robots(RobotFileParser):

    def __init__(self):
        RobotFileParser.__init__(self)
        self.maps = dict()
        self.maps_list = []
        self.lines_robots = None

    def set_url_ext(self, url_base):
        self.url_base = get_base_url(url_base)
        self.url_base = parse.urljoin(self.url_base, 'robots.txt')
        self.set_url(self.url_base)

    def site_maps_ext(self, urlopener=None):
        """
        Создает сдоварь user-agent: sitemap
        и список.
        """

        response = urlopen(self.url_base)
        code = response.getcode()
        raw = response.read()

        user_agent = '*'

        self.lines_robots = raw.decode("utf-8").splitlines()

        for line in self.lines_robots:
            if len(line) > 1:
                parts = line.split(':')
                parts[0] = parts[0].strip().lower()
                parts[1] = parse.unquote(parts[1].strip().lower())
                if parts[0] == 'user-agent':
                    user_agent = parts[1]
                if parts[0] == 'sitemap':
                    self.maps[user_agent] = parts[1] + ':' + parts[2]
                    self.maps_list.append(self.maps[user_agent])
