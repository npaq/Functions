from setuptools import setup, find_packages

setup(
    name='rdo_functions',
    version='0.0.2',
    description='Private package with helper functions for radiological consequences calculations',
    url='git@github.com/npaq/Functions.git',
    author='Nicolas Paquet',
    author_email='nicolas.paquet@tractebel.engie.com',
    license='LICENSE.txt',
    zip_safe=False,
    packages=find_packages(include=['rdo_functions', 'rdo_functions.*']),
	install_requires=['pandas']
)
