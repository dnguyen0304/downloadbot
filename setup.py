#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

if __name__ == '__main__':
    package_name = 'downloadbot'

    description = 'A Pokemon Showdown web scraper.'

    with open('./README.md', 'r') as file:
        long_description = file.read()

    setuptools.setup(name=package_name,
                     version='0.1.0',
                     description=description,
                     long_description=long_description,
                     url='https://github.com/dnguyen0304/downloadbot.git',
                     author='Duy Nguyen',
                     author_email='dnguyen0304@gmail.com',
                     license='MIT',
                     classifiers=['Programming Language :: Python :: 3.6'],
                     packages=setuptools.find_packages(exclude=['*.tests']),
                     test_suite='nose.collector',
                     tests_require=['nose'],
                     include_package_data=True)
