from urllib.parse import urlsplit, urlunsplit


def get_base_url(url):
    parts = list(urlsplit(url))
    parts[2] = ''
    parts[3] = ''
    parts[4] = ''
    url = urlunsplit(parts)
    return url
