from urllib.request import urlopen
from urllib.parse import urlsplit
import warnings


class XMLload:

    def __init__(self, url):
        self.url = url
        self.xml_file = None

    def load(self):
        xml_file = urlsplit(self.url)
        self.xml_file = 'tmp' + xml_file.path.rstrip()
        with urlopen(self.url) as remote, open(self.xml_file, 'wb') as local:
                local.write(remote.read())
