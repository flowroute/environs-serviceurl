import pytest

from environs import EnvError
from environs_serviceurl import service_url

basic_cases = pytest.mark.parametrize(('url', 'expected'), [
    # Basic null scenario
    ('', {
        'host': None,
        'port': None,
        'user': None,
        'password': None,
        'extras': None,
    }),
    # Simple URL, no params, missing fields.
    ('http://example.com', {
        'host': 'example.com',
        'port': None,
        'user': None,
        'password': None,
        'extras': None,
    }),
    #  All the possibile url fields, plus path-extra and query params.
    ('tcp://a_user:a_pass@example.com:1234/silly?spam=eggs&parrots=pining', {
        'host': 'example.com',
        'port': 1234,
        'user': 'a_user',
        'password': 'a_pass',
        'extras': 'silly',
        'spam': 'eggs',
        'parrots': 'pining',
    }),
    # Multiple params with same key should return last key's value.
    ('http://example.com?spam=eggs&spam=spam', {
        'host': 'example.com',
        'port': None,
        'user': None,
        'password': None,
        'extras': None,
        'spam': 'spam',
    }),
    # URL encoded values work
    ('http://:passwith%23@example.com?dir=%2f', {
        'host': 'example.com',
        'port': None,
        'user': None,
        'password': 'passwith#',
        'extras': None,
        'dir': '/',
    }),
    # Throws an error on an unparsable thing.
    ([1], EnvError),
])

default_cases = pytest.mark.parametrize(('url', 'defaults', 'expected'), [
    # Empty default doesn't break.
    ('', {}, {
        'host': None,
        'port': None,
        'user': None,
        'password': None,
        'extras': None,
    }),
    # Simple default appears if url doesn't have that fied.
    ('', {'host': 'localhost'}, {
        'host': 'localhost',
        'port': None,
        'user': None,
        'password': None,
        'extras': None,
    }),
    # Default doesn't appear if url has field.
    ('http://example.com', {'host': 'localhost'}, {
        'host': 'example.com',
        'port': None,
        'user': None,
        'password': None,
        'extras': None,
    }),
    # Default and non-default fields appear together
    ('http://example.com', {'port': 80}, {
        'host': 'example.com',
        'port': 80,
        'user': None,
        'password': None,
        'extras': None,
    }),
    # Defaults for extras/query params work
    ('http://example.com', {'spam': 'eggs'}, {
        'host': 'example.com',
        'port': None,
        'user': None,
        'password': None,
        'extras': None,
        'spam': 'eggs',
    }),
    # Param defaults are overridden.
    ('http://example.com?spam=lovelyspam', {'spam': 'eggs'}, {
        'host': 'example.com',
        'port': None,
        'user': None,
        'password': None,
        'extras': None,
        'spam': 'lovelyspam',
    }),
    # Defaults don't prevent errors on unparseable values.
    ([1], {'host': 'localhost'}, EnvError),
])

extras_cases = pytest.mark.parametrize(('url', 'extras', 'expected'), [
    # When we have an extras name, we get that name in the return, not 'extras'
    ('http://example.com/gandalf', 'wizard', {
        'host': 'example.com',
        'port': None,
        'user': None,
        'password': None,
        'wizard': 'gandalf',
    }),
])


@basic_cases
def test_basics(url, expected):
    if type(expected) == type(type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            service_url(url) == expected
    else:
        assert service_url(url) == expected


@default_cases
def test_defaults(url, defaults, expected):
    if type(expected) == type(type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            service_url(url, defaults=defaults) == expected
    else:
        assert service_url(url, defaults=defaults) == expected


@extras_cases
def test_extras_name(url, extras, expected):
    if type(expected) == type(type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            service_url(url, extras_name=extras) == expected
    else:
        assert service_url(url, extras_name=extras) == expected
