from urllib.request import urlopen
from urllib.parse import urlsplit, urlparse
import warnings
import time
from pathlib import Path


class XMLload:

    def __init__(self, url=None):
        self.url = url
        self.xml_file_name = None

    def load(self, url=None, dir="tmp/"):
        if url is not None:
            self.url = url

        xml_file = urlsplit(self.url)
        xml_file = str(time.time()) + xml_file.path.split('/')[-1]
        self.xml_file_name = dir + xml_file.rstrip()

        with urlopen(self.url) as remote, open(self.xml_file_name, 'wb') as local:
                local.write(remote.read())

    def unlink(self):
        p = Path(self.xml_file_name)
        p.unlink()
