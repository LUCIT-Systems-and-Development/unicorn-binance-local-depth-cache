#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_depth_cache.py
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
from lucit_licensing_python.exceptions import NoValidatedLucitLicense
import asyncio
import logging
import os
import time

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def use_a_depth_cache():
    with BinanceLocalDepthCacheManager(exchange="binance.com") as ubldc:
        print(f"UBLDC version {ubldc.get_version()}")
        market = 'BTCUSDT'
        ubldc.create_depth_cache(markets=market)
        while True:
            time.sleep(1)
            print(f"is_synchronized: {ubldc.is_depth_cache_synchronized(market)}")
            try:
                print(f"Top 10 asks: {ubldc.get_asks(market=market)[:10]}")
                print(f"Top 10 bids: {ubldc.get_bids(market=market)[:10]}")
            except DepthCacheOutOfSync as error_msg:
                print(f"Out of sync! Please wait ... ({error_msg})")
                await asyncio.sleep(1)

try:
    asyncio.run(use_a_depth_cache())
except NoValidatedLucitLicense as e:
    print(f"\r\nERROR: {e}")
    print("Gracefully stopping ...")
except KeyboardInterrupt:
    print("\r\nGracefully stopping ...")

