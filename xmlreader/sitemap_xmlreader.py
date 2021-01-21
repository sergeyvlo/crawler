from xml.etree.ElementTree import iterparse
from urllib.error import URLError, HTTPError
from http.client import InvalidURL
from pathlib import Path

from .xmlload import XMLload
from .xmlrecord import XMLRecord

from urlopener import openerconfig


class SitemapXML:

    def __init__(self, urlopener):
        self.sitemap_xml = None             # Имя XML файла
        self.url_sitemap = []               # Срисок url файлов XML sitemap
        self.flag_load = False              # Чтобы повторно не загружать XML sitemap
        self.xml_is_load = True             # Загружен XML файл
        self.xml_ns = None                  # namespase XML
        self.load_xml_file = XMLload(urlopener)     # Загружает XML файл на диск

    def make_sitemap_url(self):
        """Формирует список URL-ов файлов XML sitemap"""
        data = iterparse(self.sitemap_xml, ['start', 'end'])
        self._xml_namespace()

        for (event, node) in data:
            node_name = node.tag.split(self.xml_ns)[1]
            if node_name == 'sitemap' and event == 'end':

                # Загрузить URL файлов sitemaps
                record = XMLRecord(node, self.xml_ns)
                try:
                    self.url_sitemap.append(record.loc)
                except AttributeError:
                    print('Нет атрибута: record.loc')
                self.flag_load = True   # Разрешить загружать xml файлы sitemap

            elif node_name == 'urlset' and event == 'start':
                self.url_sitemap.append(self.sitemap_xml)
                continue

        # Удалить XML файл
        if self.flag_load:
            self.load_xml_file.unlink()

    def extract_url_from_sitemap(self):
        for url in self.url_sitemap:
            # Не загружать повторно sitemap.xml, если он один
            if self.flag_load:
                self.xml_load(url)

            if self.xml_is_load:
                data = iterparse(self.sitemap_xml, ['start', 'end'])
                self._xml_namespace()
                for (event, node) in data:
                    node_name = node.tag.split(self.xml_ns)[1]
                    if node_name == 'url' and event == 'end':
                        record = XMLRecord(node, self.xml_ns)
                        try:
                            yield record.loc
                        except AttributeError:
                            print('Нет атрибута: record.loc')

                # Удалить XML файл
                self.load_xml_file.unlink()

    def xml_load(self, url):
        """Физически загружает файл на диск"""
        try:
            self.load_xml_file.load(url)
        except (URLError, HTTPError, InvalidURL) as e:
            print('Невозможно загрузить файл:', url, e)
            self.xml_is_load = False

        self.sitemap_xml = self.load_xml_file.xml_file_name

    def _xml_namespace(self):
        """Получить namespase"""
        ns = []
        data = iterparse(self.sitemap_xml, ['start-ns', 'end-ns'])
        for (event, node) in data:
            if event == 'start-ns':
                ns.append(node[1])
                continue
        self.xml_ns = '{' + ns[0] + '}'
