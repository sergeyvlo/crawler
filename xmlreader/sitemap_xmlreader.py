from xml.etree.ElementTree import iterparse
from urllib.error import URLError, HTTPError
from http.client import InvalidURL

from .xmlload import XMLload
from .xmlrecord import XMLRecord
from urlopener.robots import Robots
from urlopener import openerconfig


class SitemapXML:

    def __init__(self):
        self.EVENT_NAME = ['start', 'end']
        self.sitemap_xml = None
        self.url_sitemap = []
        self.url_sitemap_parser = None      # URL sitemap из robots.txt

    def sitemap_load(self, url_base):
        """Извлекает из robots.txt url xml файла карты
           Загружает его на диск
        """
        parser = Robots()
        parser.set_url_ext(url_base)
        parser.site_maps_ext()
        self.url_sitemap_parser = parser.maps[openerconfig.USER_AGENT_ROBOTS]
        self.xml_load(self.url_sitemap_parser)

        return self.sitemap_xml

    def make_sitemap_url(self):
        data = iterparse(self.sitemap_xml, self.EVENT_NAME)

        for (event, node) in data:
            node_name = node.tag.split(openerconfig.NAME_SPASE)[1]
            if node_name == 'sitemap' and event == 'start':

                # Загрузить URL файлов sitemaps
                record = XMLRecord(node, openerconfig.NAME_SPASE)
                try:
                    self.url_sitemap.append(record.loc)
                except AttributeError:
                    print('Нет атрибута')

            elif node_name == 'urlset' and event == 'start':
                self.url_sitemap.append(self.url_sitemap_parser)
                continue

    def xml_load(self, url):
        """Физически загружает файл на диск"""
        xml_file = XMLload()

        try:
            xml_file.load(url)
        except (URLError, HTTPError, InvalidURL):
            print('Нет такого файла')

        self.sitemap_xml = xml_file.xml_file_name
