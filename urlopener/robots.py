"""
Обрабатывает robots.txt
Базовый url для интернациональных доменов должен декодироваться
в idn заранее
"""
from urllib.robotparser import RobotFileParser
from urllib.request import urlopen
from urllib import parse

from .utils import get_base_url

class Robots(RobotFileParser):

    def __init__(self):
        RobotFileParser.__init__(self)
        self.url_robots = None
        self.maps = dict()
        self.maps_list = []
        self.lines_robots = None

    def set_url_ext(self, url_base):
        self.url_robots = get_base_url(url_base)
        self.url_robots = parse.urljoin(self.url_robots, 'robots.txt')
        self.set_url(self.url_robots)

    def site_maps_ext(self, raw):
        """
        Создает сдоварь user-agent: sitemap
        и список.
        """
        user_agent = '*'

        self.lines_robots = raw.splitlines()

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