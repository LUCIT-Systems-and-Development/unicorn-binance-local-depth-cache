#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_update_interval.py
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

from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheOutOfSync
import logging
import os
import time

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

market = 'BTCUSDT'

ubldc = BinanceLocalDepthCacheManager(exchange="binance.com")
# ubldc = BinanceLocalDepthCacheManager(exchange="binance.com-testnet")

# update_speed tells binance endpoints the frequency in which updates are sent
# the value is in milliseconds, possible values are different for each endpint:
# https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/wiki/update_intervals

ubldc.create_depth_cache(markets=market, update_interval=100)

while True:
    print(f"is_synchronized: {ubldc.is_depth_cache_synchronized(market)}")
    try:
        print(f"Top 10 asks: {ubldc.get_asks(market=market)[:10]}")
        print(f"Top 10 bids: {ubldc.get_bids(market=market)[:10]}")
    except DepthCacheOutOfSync as error_msg:
        print(f"ERROR: {error_msg}")
    time.sleep(1)

