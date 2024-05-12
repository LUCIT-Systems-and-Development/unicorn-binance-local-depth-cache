#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: test_cache.py
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
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

market = 'BTCUSDT'
exchange = "binance.com-futures"

ubldc = BinanceLocalDepthCacheManager(exchange=exchange, update_interval=100)
ubldc.create_depth_cache(markets=market)

while True:
    try:
        top_asks = ubldc.get_asks(market=market)[:4]
        top_bids = ubldc.get_bids(market=market)[:4]
    except DepthCacheOutOfSync:
        top_asks = "Out of sync!"
        top_bids = "Out of sync!"
    depth = (f"depth_cache is in sync: {ubldc.is_depth_cache_synchronized(market)}\r\n " 
             f"top 4 asks: {top_asks}\r\n "
             f"top 4 bids: {top_bids}")
    ubldc.print_summary(add_string=depth)
    time.sleep(0.2)
