#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheOutOfSync
from unicorn_binance_rest_api import BinanceRestApiManager
import asyncio
import logging
import os
import time

exchange = "binance.com-futures"
update_interval_ms = 100

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def main():
    all_markets: list = [item['symbol'] for item in ubra.get_all_tickers() if item['symbol'].endswith("USDT")]
    used_markets: list = []

    markets = all_markets[0:1]
    used_markets.extend(markets)
    print(f"Starting DepthCache for market: {markets}")
    ubldc.create_depth_cache(markets=markets)
    markets = all_markets[1:3]
    used_markets.extend(markets)
    print(f"Starting DepthCaches for markets: {markets}")
    ubldc.create_depth_cache(markets=markets)

    time.sleep(10)

    ubldc.stop_depth_cache(markets=used_markets)
    while ubldc.is_stop_request() is False:
        add_string = (f"used_weight={ubra.get_used_weight()}\r\n "
                      f"---------------------------------------------------------------------------------------------")
        for market in used_markets:
            try:
                top_asks = ubldc.get_asks(market=market)[:4]
                top_bids = ubldc.get_bids(market=market)[:4]
            except DepthCacheOutOfSync:
                top_asks = "Out of sync!"
                top_bids = "Out of sync!"
            depth = (f"depth_cache '{market}' is in sync: {ubldc.is_depth_cache_synchronized(market=market)}\r\n " 
                     f"top 4 asks: {top_asks}\r\n "
                     f"top 4 bids: {top_bids}")
            add_string = f"{add_string}\r\n {depth}"
        ubldc.print_summary(add_string=add_string)
        time.sleep(0.5)


ubra = BinanceRestApiManager(exchange=exchange)
with BinanceLocalDepthCacheManager(exchange=exchange,
                                   ubra_manager=ubra,
                                   update_interval=update_interval_ms) as ubldc:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\r\nGracefully stopping ...")
    except Exception as e:
        print(f"\r\nERROR: {e}")
        print("Gracefully stopping ...")
