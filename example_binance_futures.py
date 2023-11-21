#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_binance_futures.py
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
from unicorn_binance_websocket_api import BinanceWebSocketApiManager
import logging
import os
import time

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

market = 'BTCUSDT'
exchange = "binance.com-futures"

ubwa = BinanceWebSocketApiManager(exchange=exchange, enable_stream_signal_buffer=True)
ubldc = BinanceLocalDepthCacheManager(exchange=exchange, ubwa_manager=ubwa)
ubldc.create_depth_cache(markets=market)

while True:
    try:
        top_asks = ubldc.get_asks(market=market)[:3]
        top_bids = ubldc.get_bids(market=market)[:3]
    except DepthCacheOutOfSync:
        top_asks = "Out of sync!"
        top_bids = "Out of sync!"
    depth = f"top 3 asks: {top_asks}\r\n top 3 bids: {top_bids}"
    ubldc.ubwa.print_summary(add_string=depth)
    time.sleep(1)

