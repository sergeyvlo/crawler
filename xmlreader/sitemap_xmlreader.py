from xml.etree.ElementTree import iterparse
from urllib.error import URLError, HTTPError
from http.client import InvalidURL
from pathlib import Path

from .xmlload import XMLload
from .xmlrecord import XMLRecord

from urlopener import openerconfig


class SitemapXML:

    def __init__(self):
        self.sitemap_xml = None
        self.url_sitemap = []
        self.url_sitemap_parser = None      # URL sitemap из robots.txt
        self.flag_load = False              # Чтобы повторно не загружать XML sitemap
        self.xml_is_load = True

    def sitemap_load(self, url_xml_sitemap):
        """Загружает на диск файл XML sitemap"""
        self.url_sitemap_parser = url_xml_sitemap
        self.xml_load(self.url_sitemap_parser)

    def make_sitemap_url(self):
        """Формирует список URL-ов файлов XML sitemap"""
        data = iterparse(self.sitemap_xml, ['start', 'end'])

        for (event, node) in data:
            node_name = node.tag.split(openerconfig.NAME_SPASE)[1]
            if node_name == 'sitemap' and event == 'start':

                # Загрузить URL файлов sitemaps
                record = XMLRecord(node, openerconfig.NAME_SPASE)
                try:
                    self.url_sitemap.append(record.loc)
                except AttributeError:
                    print('Нет атрибута: record.loc')
                self.flag_load = True   # Разрешить загружать xml файлы sitemap

            elif node_name == 'urlset' and event == 'start':
                self.url_sitemap.append(self.url_sitemap_parser)
                continue

        if self.flag_load:
            p = Path(self.sitemap_xml)
            p.unlink()

    def extract_url_from_sitemap(self, urlopener):
        for url in self.url_sitemap:
            # Не загружать повторно sitemap.xml, если он один
            if self.flag_load:
                self.xml_load(url)

            if self.xml_is_load:
                data = iterparse(self.sitemap_xml, ['start', 'end'])
                for (event, node) in data:
                    node_name = node.tag.split(openerconfig.NAME_SPASE)[1]
                    if node_name == 'url' and event == 'start':

                        record = XMLRecord(node, openerconfig.NAME_SPASE)
                        try:
                            #print(record.loc)
                            response = urlopener.urlopen(record.loc)
                            if response['redirect'] is not None:
                                print(response['redirect'])

                            if response['response'] is not None:
                                print(response['response']['code'], response['response']['url'],
                                      response['response']['msg'])

                            if response['error'] is not None:
                                print(response['error'])
                        except AttributeError:
                            print('Нет атрибута: record.loc')

                # Удалить XML файл
                p = Path(self.sitemap_xml)
                p.unlink()

    def xml_load(self, url):
        """Физически загружает файл на диск"""
        xml_file = XMLload()

        try:
            xml_file.load(url)
        except (URLError, HTTPError, InvalidURL) as e:
            print('Невозможно загрузить файл:', url, e)
            self.xml_is_load = False

        self.sitemap_xml = xml_file.xml_file_name
