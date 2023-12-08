#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: setup.py
#
# Part of ‘UNICORN Binance Local Depth Cache’
# Project website: https://www.lucit.tech/unicorn-binance-local-depth-cache.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache
# Documentation: https://unicorn-binance-local-depth-cache.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-local-depth-cache
# LUCIT Online Shop: https://shop.lucit.services/software
#
# License: LSOSL - LUCIT Synergetic Open Source License
# https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/blob/master/LICENSE
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2022-2023, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

from setuptools import setup
from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
     ext_modules=cythonize(
        ['unicorn_binance_local_depth_cache/__init__.py',
         'unicorn_binance_local_depth_cache/exceptions.py',
         'unicorn_binance_local_depth_cache/manager.py'],
        annotate=False),
     name='unicorn-binance-local-depth-cache',
     version="1.0.0",
     author="LUCIT Systems and Development",
     author_email='info@lucit.tech',
     url="https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache",
     description="A local Binance DepthCache Manager for Python by LUCIT that supports multiple depth caches in one "
                 "instance in a easy, fast, flexible, robust and fully-featured way.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     license='LSOSL - LUCIT Synergetic Open Source License',
     install_requires=['lucit-licensing-python>=1.8.1', 'Cython', 'requests', 'unicorn-binance-websocket-api>=2.1.1',
                       'unicorn-binance-rest-api>=2.1.2'],
     keywords='binance, depth cache',
     project_urls={
         'Documentation': 'https://unicorn-binance-local-depth-cache.docs.lucit.tech',
         'Wiki': 'https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/wiki',
         'Author': 'https://www.lucit.tech',
         'Changes': 'https://unicorn-binance-local-depth-cache.docs.lucit.tech/changelog.html',
         'License': 'https://unicorn-binance-local-depth-cache.docs.lucit.tech/license.html',
         'Issue Tracker': 'https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/issues',
         'Chat': 'https://gitter.im/unicorn-binance-suite/unicorn-binance-local-depth-cache',
         'Telegram': 'https://t.me/unicorndevs',
         'Get Support': 'https://www.lucit.tech/get-support.html',
         'LUCIT Online Shop': 'https://shop.lucit.services/software',
     },
     python_requires='>=3.7.0',
     package_data={'': ['unicorn_binance_local_depth_cache/*.so',
                        'unicorn_binance_local_depth_cache/*.dll']},
     classifiers=[
         "Development Status :: 5 - Production/Stable",
         "Programming Language :: Python :: 3.7",
         "Programming Language :: Python :: 3.8",
         "Programming Language :: Python :: 3.9",
         "Programming Language :: Python :: 3.10",
         "Programming Language :: Python :: 3.11",
         "Programming Language :: Python :: 3.12",
         "License :: Other/Proprietary License",
         'Intended Audience :: Developers',
         "Intended Audience :: Financial and Insurance Industry",
         "Intended Audience :: Information Technology",
         "Intended Audience :: Science/Research",
         "Operating System :: OS Independent",
         "Topic :: Office/Business :: Financial :: Investment",
         'Topic :: Software Development :: Libraries :: Python Modules',
     ],
)
