"""
Обрабатывает robots.txt
Базовый url для интернациональных доменов должен декодироваться
в idn заранее
"""
from urllib.robotparser import RobotFileParser
from urllib import parse

from .utils import get_base_url

class Robots(RobotFileParser):

    def make_robots(self, url_base):
        self.url_base = get_base_url(url_base)
        self.url_base = parse.urljoin(self.url_base, 'robots.txt')
        self.set_url(self.url_base)

    def site_maps_ext(self):
        pass
