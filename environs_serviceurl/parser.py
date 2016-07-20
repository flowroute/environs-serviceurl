try:
    from urllib.parse import urlparse, unquote, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs
    from urllib import unquote

from environs import EnvError


def service_url(url, defaults={}, extras_name='extras'):
    """
    environs handler for URLS, turning a url string into a dictionary
    of its component parts.
    """
    try:
        parsed = urlparse(url)
    except Exception:
        raise EnvError(
            'Service URLS look like: servtype://user:pass@host:port/' +
            extras_name + '?param1=Foo&param2=Bar')

    conf = {
        'host': unquote(parsed.hostname) if parsed.hostname else None,
        'port': parsed.port,
        'user': unquote(parsed.username) if parsed.username else None,
        'password': unquote(parsed.password) if parsed.password else None,
        extras_name: unquote(parsed.path)[1:] if parsed.path else None,
    }

    # If we get multiple values for a given key, use the last.
    extra_params = {k: v[-1] for k, v in parse_qs(parsed.query).items()}
    conf.update(extra_params)

    missing_defaults = {k: v for k, v in defaults.items()
                        if k not in conf or conf[k] is None}
    conf.update(missing_defaults)

    return conf
