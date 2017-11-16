#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

if __name__ == '__main__':
    package_name = 'downloadbot'

    description = 'A Pokemon Showdown web scraper.'

    with open('./README.md', 'r') as file:
        long_description = file.read()

    install_requires = [
        # This package is needed by the infrastructure layer to
        # implement consumers that receive messages from AWS Simple
        # Queue Service (SQS).
        'boto3==1.4.7',
        # This package is needed by the application layer to
        # implement bots that interact with web pages.
        'selenium==3.5.0',
        # This package is needed by the library layer to provide Python
        # 2 and 3 compatibility.
        'six==1.11.0']

    setuptools.setup(name=package_name,
                     version='0.1.1',
                     description=description,
                     long_description=long_description,
                     url='https://github.com/dnguyen0304/downloadbot.git',
                     author='Duy Nguyen',
                     author_email='dnguyen0304@gmail.com',
                     license='MIT',
                     classifiers=['Programming Language :: Python :: 3.6'],
                     packages=setuptools.find_packages(exclude=['*.tests']),
                     install_requires=install_requires,
                     test_suite='nose.collector',
                     tests_require=['mock', 'nose'],
                     include_package_data=True)
