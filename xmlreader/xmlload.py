from urllib.request import urlopen
from urllib.parse import urlsplit
import time
from pathlib import Path


class XMLload:

    def __init__(self, urlopener, url=None):
        self.url = url
        self.xml_file_name = None
        self.urlopener = urlopener      # URL открывалка

    def load(self, url=None, dir="tmp/"):
        if url is not None:
            self.url = url

        xml_file = urlsplit(self.url)
        xml_file = str(time.time()) + xml_file.path.split('/')[-1]
        self.xml_file_name = dir + xml_file.rstrip()

        self.urlopener.urlopen(self.url)

        with open(self.xml_file_name, 'wb') as local:
            local.write(self.urlopener.response.read())

    def unlink(self):
        p = Path(self.xml_file_name)
        p.unlink()
