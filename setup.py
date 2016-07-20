from setuptools import setup, find_packages


requires = {
    'setup': [
    ],
    'install': [
        'environs',
    ],
    'tests': [
        'pytest',
        'pytest-cov',
        'pytest-flake8',
    ],
}

requires['all'] = list({dep for deps in requires.values() for dep in deps})


def readme():
    with open('README.rst', 'r') as readme_file:
        return readme_file.read()

setup(
    name='environs-serviceurl',
    version='1.0.1',
    description='Add service URL parsing support for environs',
    long_description=readme(),
    url='http://github.com/flowroute/environs-serviceurl',
    author='Dan Root',
    author_email='rootdan+pypi@gmail.com',
    license='MIT',

    packages=find_packages(exclude=['test']),
    setup_requires=requires['setup'],
    install_requires=requires['install'],
    tests_require=requires['tests'],
    extras_require=requires,
    include_package_data=True,
    zip_safe=False,
    platforms='any',

    keywords=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
