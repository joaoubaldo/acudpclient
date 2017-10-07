import os

from setuptools import setup, find_packages

from acudpclient import VERSION

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
  README = f.read()
with open(os.path.join(here, 'requirements.txt')) as f:
  requires = f.read().splitlines()

tests_require = requires + [
    'pylint'
]

version = os.getenv('BUILD_VERSION', VERSION)

setup(name='acudpclient',
    version=version,
    description='Assetto Corsa UDP Client',
    long_description=README + '\n',
    classifiers=[
        "Programming Language :: Python"
    ],
    author='Joao Coutinho',
    author_email='me@joaoubaldo.com',
    url='https://b.joaoubaldo.com',
    keywords='assetto-corsa dedicated-server client udp',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="tests"
)
