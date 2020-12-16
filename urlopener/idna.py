from urllib.parse import quote, urlsplit, urlunsplit, unquote


def idna_encode(url):
    parts = list(urlsplit(url))

    try:
        url.encode('ascii')
    except UnicodeEncodeError:
        parts[1] = parts[1].encode('idna').decode('ascii')

    parts[0] = quote(parts[0], safe=':/?&=')
    parts[2] = quote(parts[2], safe=':/?&=')
    parts[3] = quote(parts[3], safe=':/?&=')
    parts[4] = quote(parts[4], safe=':/?&=')
    url = urlunsplit(parts)
    return url


def idna_decode(url):
    parts = list(urlsplit(url))

    parts[1] = parts[1].encode('ascii').decode('idna')
    parts[0] = unquote(parts[0])
    parts[2] = unquote(parts[2])
    parts[3] = unquote(parts[3])
    parts[4] = unquote(parts[4])

    url = urlunsplit(parts)
    return url
