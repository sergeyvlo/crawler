import functools, re, urlparse
import ssl

old_match_hostname = ssl.match_hostname

@functools.wraps(old_match_hostname)
def match_hostname_bugfix(cert, hostname):
    m = re.search(r':\d+$',hostname)  # hostname:port
    if m is not None:
        o = urlparse.urlparse('https://' + hostname)
        hostname = o.hostname
    old_match_hostname(cert, hostname)

ssl.match_hostname = match_hostname_bugfix
