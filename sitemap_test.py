from xml.etree.ElementTree import iterparse

from urlopener import Urlopener, openerconfig
from urlopener.idna import idna_encode
from xmlreader import SitemapXML
from xmlreader.xmlrecord import XMLRecord

#url_base = "http://www.fish.customweb.ru/"
#url_base = 'https://bagaznik-darom.ru/'
url_base = 'https://www.citilink.ru/'



url_base = idna_encode(url_base)

sitemap_xml = SitemapXML()
xml_file = sitemap_xml.sitemap_load(url_base)
sitemap_xml.make_sitemap_url()

print(sitemap_xml.url_sitemap)
