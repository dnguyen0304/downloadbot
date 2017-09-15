#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

if __name__ == '__main__':
    package_name = 'roomlistwatcher'

    description = 'A Pokemon Showdown web scraper.'

    with open('./README.md', 'r') as file:
        long_description = file.read()

    install_requires = [
        # This package is needed by the infrastructure layer to
        # implement producers that send their data to AWS Simple Queue
        # Service (SQS).
        'boto3==1.4.7',
        # This package is needed by the application layer to use
        # enumerations.
        'enum34==1.1.6',
        # This package is needed by the application layer to
        # implement scrapers that extract data from web pages.
        'selenium==3.3.3']

    setuptools.setup(name=package_name,
                     version='0.1.0',
                     description=description,
                     long_description=long_description,
                     url='https://github.com/dnguyen0304/room-list-watcher.git',
                     author='Duy Nguyen',
                     author_email='dnguyen0304@gmail.com',
                     license='MIT',
                     classifiers=['Programming Language :: Python :: 2.7'],
                     packages=setuptools.find_packages(exclude=['*.tests']),
                     install_requires=install_requires,
                     test_suite='nose.collector',
                     tests_require=['mock', 'nose'],
                     include_package_data=True)
