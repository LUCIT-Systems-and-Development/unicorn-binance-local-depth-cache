#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheOutOfSync
import asyncio
import logging

logging.basicConfig(level=logging.ERROR, filename='dc.log')


async def main():
    limit_count: int = 3
    ubra = ubldc.get_ubra_manager()
    exchange_info = ubra.get_exchange_info()
    markets = []
    for item in exchange_info['symbols']:
        if item['status'] == "TRADING":
            markets.append(item['symbol'])
    ubldc.create_depthcache(markets=markets[:600])
    while ubldc.is_stop_request() is False:
        add_string = f"---------------------------------------------------------------------------------------------"
        working = []
        not_working = []
        for market in markets[:600]:
            try:
                top_asks_limit = ubldc.get_asks(market=market, limit_count=limit_count)
                top_bids_limit = ubldc.get_bids(market=market, limit_count=limit_count)
                working.append(market)
                depth = (f"depth_cache '{market}' is in sync: {ubldc.is_depth_cache_synchronized(market=market)} "
                         f" top {limit_count} asks: {top_asks_limit} | top {limit_count} bids: {top_bids_limit}")
                add_string = f"{add_string}\r\n {depth}"
            except DepthCacheOutOfSync:
                not_working.append(market)
        add_string += f"\r\n Working: {len(working)} | Not Working: {len(not_working)}"
        ubldc.print_summary(add_string=add_string)
        await asyncio.sleep(60)

with BinanceLocalDepthCacheManager(exchange="binance.com") as ubldc:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\r\nGracefully stopping ...")

