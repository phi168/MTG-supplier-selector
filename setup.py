#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2021 Thore Mainart Bücking
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
from setuptools import setup, setuptools


__author__ = "Thore M. Bücking"
__version__= "0.0.1"


def readme():
    with open('README.rst', encoding="UTF-8") as f:
        return f.read()


if sys.version_info < (3, 7, 6):
    sys.exit('Python < 3.7.6 is not supported!')


setup(name='mtgss',
      version=__version__,
      description='Magic-the-gatheric supplier selector for list of cards. Selecting optimal combination of suppliers from lilianamarket.co.uk and magicmadhouse.co.uk',
      long_description=readme(),
      url='http://github.com/,
      author='Thore M. Bücking',
      author_email='thore@buecking.me',
      license='MIT',
      packages=setuptools.find_packages(exclude=["tests.*", "tests"]),
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
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      keywords="magic-the-gathering mtg card buy",
      zip_safe=False)
