from setuptools import setup, find_packages

setup(
    name='functions',
    version='0.0.1',
    description='Private package with helper functions for radiological consequences calculations',
    url='git@github.com:npaq/Functions.git',
    author='Nicolas Paquet',
    author_email='nicolas.paquet@tractebel.engie.com',
    license='LICENSE.txt',
    zip_safe=False,
    packages=find_packages(include=['functions', 'functions.*']))

