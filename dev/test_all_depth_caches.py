#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: test_all_depth_caches.py
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
#
# To use this library you need a valid UNICORN Binance Suite License:
# https://medium.lucit.tech/87b0088124a8

import logging
import os
import time
from unicorn_binance_rest_api import BinanceRestApiManager
from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheOutOfSync

logging.getLogger()
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

exchange = "binance.com"

with BinanceRestApiManager(exchange=exchange) as ubra:
    markets = [item['symbol'] for item in ubra.get_all_tickers()]

markets = markets[0:30]
print(f"Starting Depth Cache Demo with {len(markets)} markets ...")

ubldc = BinanceLocalDepthCacheManager(exchange=exchange)

print(f"Create Depth Caches ...")
for market in markets:
    ubldc.create_depth_cache(markets=market, update_interval=1000)
    time.sleep(10)
print(f"Running ...")

try:
    while True:
        time.sleep(0.2)
        print(f"{ubldc.get_list_of_depth_caches()=:}")

        print(f"\r\n{str(markets[0])} is_synchronized: {ubldc.is_depth_cache_synchronized(str(markets[0]))}")
        try:
            print(f"Top 10 asks: {ubldc.get_asks(market=markets[0])[:10]}")
            print(f"Top 10 bids: {ubldc.get_bids(market=markets[0])[:10]}")
        except DepthCacheOutOfSync as error_msg:
            print(f"Please wait ... ")
            time.sleep(1)

        print(f"\r\n{str(ubldc.get_list_of_depth_caches()[-1])} is_synchronized: "
              f"{ubldc.is_depth_cache_synchronized(str(ubldc.get_list_of_depth_caches()[-1]))}")
        try:
            print(f"Top 10 asks: {ubldc.get_asks(market=ubldc.get_list_of_depth_caches()[-1])[:10]}")
            print(f"Top 10 bids: {ubldc.get_bids(market=ubldc.get_list_of_depth_caches()[-1])[:10]}")
        except DepthCacheOutOfSync as error_msg:
            print(f"Please wait ... ")
            time.sleep(1)
except KeyboardInterrupt:
    print("Gracefully stopping, please wait a few seconds ...")
ubldc.stop_manager()
