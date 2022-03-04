#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_version_of_this_package.py
#
# Part of ‘UNICORN Binance Local Depth Cache’
# Project website: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache
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

import unicorn_binance_local_depth_cache

# create instance of BinanceWebSocketApiManager
ubldc = unicorn_binance_local_depth_cache.BinanceLocalDepthCacheManager()

# get version of the used UNICORN Binance WebSocket API
if ubldc.is_update_available():
    print("Please upgrade to " + ubldc.get_latest_version() + ", you are on",
          ubldc.get_version())

    latest_release_info = ubldc.get_latest_release_info()
    if latest_release_info:
        print("Please download the latest release or run `pip install unicorn-binance-local-depth-cache --upgrade`: ")
        print("\ttar: " + latest_release_info["tarball_url"])
        print("\tzip: " + latest_release_info["zipball_url"])
        print("release info:")
        print(latest_release_info["body"])
else:
    print(ubldc.get_version(), "is the latest version!")

ubldc.stop_manager_with_all_depth_caches
