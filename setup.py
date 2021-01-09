#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools


__author__ = "Thore M. Bücking"
__version__= "0.0.1"


def readme():
    with open('README.md', encoding="UTF-8") as f:
        return f.read()


setuptools.setup(name='mtgss',
      version=__version__,
      description='Magic-the-gatheric supplier selector for list of cards. Selecting optimal combination of suppliers from lilianamarket.co.uk and magicmadhouse.co.uk',
      long_description=readme(),
      url='http://github.com/https://github.com/phi168/MTG-supplier-selector',
      author='Thore M. Bücking',
      author_email='thore@buecking.me',
      license='MIT',
      packages=setuptools.find_packages('src'),
      package_dir={'': 'src'},
      install_requires=[
          "lxml>=4.6.2",
          "requests>=2.23.0",
          "pandas>=1.1.5",
          "scipy>=1.5.0"
      ],
      classifiers=[
          'Environment :: Console',
          'Topic :: Games/Entertainment',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: MIT License'
      ],
      python_requires='>=3.7',)
