#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: setup.py
#
# Part of ‘UNICORN Binance Local Depth Cache’
# Project website: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache
# Documentation: https://unicorn-binance-local-depth-cache.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-local-depth-cache
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2022-2022, LUCIT Systems and Development (https://www.lucit.tech) and Oliver Zehentleitner
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import setuptools
from unicorn_binance_local_depth_cache.manager import BinanceLocalDepthCacheManager

ubldc = BinanceLocalDepthCacheManager()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='unicorn-binance-local-depth-cache',
     version=str(ubldc.get_version()),
     author="LUCIT Systems and Development",
     author_email='info@lucit.tech',
     url="https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache",
     description="",
     long_description=long_description,
     long_description_content_type="text/markdown",
     license='MIT License',
     install_requires=['requests', 'unicorn-binance-websocket-api>=1.40.5', 'unicorn-binance-rest-api'],
     keywords='binance, depth cache',
     project_urls={
        'Documentation': 'https://unicorn-binance-local-depth-cache.docs.lucit.tech',
        'Wiki': 'https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/wiki',
        'Author': 'https://www.lucit.tech',
     },
     python_requires='>=3.7.0',
     packages=setuptools.find_packages(),
     classifiers=[
         "Development Status :: 5 - Production/Stable",
         "Programming Language :: Python :: 3.7",
         "Programming Language :: Python :: 3.8",
         "Programming Language :: Python :: 3.9",
         "Programming Language :: Python :: 3.10",
         "License :: OSI Approved :: MIT License",
         'Intended Audience :: Developers',
         "Intended Audience :: Financial and Insurance Industry",
         "Intended Audience :: Information Technology",
         "Intended Audience :: Science/Research",
         "Operating System :: OS Independent",
         "Topic :: Office/Business :: Financial :: Investment",
         'Topic :: Software Development :: Libraries :: Python Modules',
     ],
)

ubldc.stop_manager_with_all_depth_caches()
