****************************************************************
evirons-serviceurl: Add service URL parsing support for environs
****************************************************************

.. image:: https://travis-ci.org/flowroute/environs-serviceurl.svg?branch=master
    :target: https://travis-ci.org/flowroute/environs-serviceurl
    :alt: Travis-CI

environs-serviceurl is a Python library that extends the
`environs <https://github.com/sloria/environs>`_ library with support for
turning service urls like ``postgres://user:pass@host:port/database`` into
Python dictionaries.


Install
-------
::

   $ pip install environs-serviceurl

Usage
-----

.. code-block:: python

    # export DATABASE_URL=postgres://me:sekrit@postgres.example.com:5432/catpics
    # export REDIS_URL=redis://redis.example.com?dbid=3

    from environs import Env
    from environs_serviceurl import service_url

    env = Env()
    env.add_parser('service_url', service_url)

    # Parse a service url.
    postgres_config = env.service_url('DATABASE_URL')
    # {'host': 'postgres.example.com',
    #  'port': 5432,
    #  'user': 'me',
    #  'password': 'sekrit',
    #  'extras': 'catpics'}

    # Give the extras a specific name
    postgres_config = env.service_url('DATABASE_URL', extras_name='database')
    # {'host': 'postgres.example.com',
    #  'port': 5432,
    #  'user': 'me',
    #  'password': 'sekrit',
    #  'database': 'catpics'}

    # Parse a service url with defaults, using query params for extra values.
    redis_config = env.service_url('REDIS_URL', 'redis://localhost/', defaults={
        'host': 'service.example.com', 'port': 6379, 'dbid': 0})
    # {'host': 'redis.example.com',
    #  'port': 6379,
    #  'user': None,
    #  'password': None,
    #  'extras': None,
    #  'dbid': '3'}



Limitations
-----------

There's currently no way to do casting on any extras or query string paramaters.
They will always be returned as string types.


License
-------

MIT.  See the `LICENSE <https://github.com/flowroute/environs-serviceurl/blob/master/LICENSE>`_ file for details.
