from urllib.error import URLError, HTTPError
from http.client import InvalidURL

from urlopener import Urlopener, openerconfig
from urlopener.idna import idna_encode
from urlopener.robots import Robots
from xmlreader import XMLload, XMLRecord
from xml.etree.ElementTree import iterparse


url_base = "https://bagaznik-darom.ru/"
EVENT_NAME = ['start', 'end']


url_base = idna_encode(url_base)

parser = Robots()
parser.set_url_ext(url_base)
parser.site_maps_ext()

xml_file = XMLload(parser.maps[openerconfig.USER_AGENT_ROBOTS])

try:
    xml_file.load()
except (URLError, HTTPError, InvalidURL):
    print('Нет такого файла')

data = iterparse(xml_file.xml_file, EVENT_NAME)

for (event, node) in data:
    node_name = node.tag.split(openerconfig.NAME_SPASE)[1]
    if  node_name == 'url' and event == 'start':

        rec = XMLRecord(node, openerconfig.NAME_SPASE)
        try:
            print(rec.loc)
        except AttributeError:
            print('Нет атрибута')
