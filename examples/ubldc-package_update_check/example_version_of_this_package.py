#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_version_of_this_package.py
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
# Copyright (c) 2022-2024, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager

with BinanceLocalDepthCacheManager(warn_on_update=False) as ubldc:
    if ubldc.is_update_available():
        print(f"Please upgrade to {ubldc.get_latest_version()} you are on {ubldc.get_version()}")
        latest_release_info = ubldc.get_latest_release_info()
        if latest_release_info:
            print(f"Please download the latest release or run `pip install unicorn-binance-local-depth-cache --upgrade`"
                  f":\r\n\ttar: {latest_release_info['tarball_url']}\r\n\tzip: {latest_release_info['zipball_url']}\r\n"
                  f"release info:\r\n{latest_release_info['body']}")
    else:
        print(ubldc.get_version(), "is the latest version!")

