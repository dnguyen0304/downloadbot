#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

if __name__ == '__main__':
    package_name = 'downloadbot.common'

    description = 'Common libraries for Pokemon Showdown web scrapers.'

    install_requires = [
        # This package is needed by the library layer to implement
        # classes that interact with web pages.
        'selenium==3.5.0',
        # This package is needed by the library layer to provide Python
        # 2 and 3 compatibility.
        'six==1.11.0']

    setuptools.setup(name=package_name,
                     version='0.1.0',
                     description=description,
                     url='https://github.com/dnguyen0304/downloadbot.git',
                     author='Duy Nguyen',
                     author_email='dnguyen0304@gmail.com',
                     license='MIT',
                     classifiers=['Programming Language :: Python :: 3.5',
                                  'Programming Language :: Python :: 3.6'],
                     packages=setuptools.find_packages(
                         include=['downloadbot', 'downloadbot.common*'],
                         exclude=['*.tests']),
                     install_requires=install_requires,
                     test_suite='nose.collector',
                     tests_require=['mock', 'nose'],
                     include_package_data=True)
