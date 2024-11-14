from setuptools import find_packages, setup

import codecs
import os



def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()

with open('app/README.md', 'r') as f:
    long_description = f.read()

VERSION = (0, 0, 1)
version = '.'.join(map(str, VERSION))

setup(
    name='quickbookspayments',
    version=version,
    author='Asad Raza',
    author_email='muhammadasadraza69@gmail.com',
    description='A Python library for accessing the QuickBooks Payments API.',
    package_dir={'': 'app'},
    packages=find_packages(where='app'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/asadraza-69/python-quickbooks-payments',
    license='MIT',
    install_requires=[
        'setuptools',
        'intuit-oauth==1.2.6',
        'requests_oauthlib>=1.3.1',
        'requests>=2.31.0',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    extras_require={
        'dev': ['pytest>=7.0', 'twine>=4.0.2'],
    },
    python_requires='>=3.10',
    # packages=find_packages(exclude=("tests",)),
)
