import sys
import os

__version__ = '1.0.0'
__nameapp__ = 'MyApp'


def opener_agent():
    app_agent = __nameapp__ + '/' + __version__
    app_agent += ' ({} {} {} {})'.format(os.uname()[0],
                                         os.uname()[2],
                                         "Python",
                                         ".".join(map(str, sys.version_info[:3])))
    return app_agent
