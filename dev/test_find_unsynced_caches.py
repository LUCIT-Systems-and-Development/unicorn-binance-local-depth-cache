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
update_interval_ms = None

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def main():
    exclude_markets: list = ['BCCUSDT', 'VENUSDT', 'TRXUSDT', 'NULSUSDT', 'TUSDUSDT', 'PAXUSDT', 'BCHABCUSDT',
                             'BCHSVUSDT', 'BTTUSDT', 'USDSUSDT']
    all_markets: list = [item['symbol'] for item in ubra.get_all_tickers() if item['symbol'].endswith("USDT")]
    used_markets: list = []

    markets = all_markets[0:30]
    used_markets.extend(markets)
    print(f"Starting DepthCaches for markets: {markets}")
    ubldc.create_depth_cache(markets=markets)

    while ubldc.is_stop_request() is False:
        add_string = (f"binance_api_status={ubra.get_used_weight(cached=True)}\r\n "
                      f"---------------------------------------------------------------------------------------------")
        list_of_synced_caches: list = []
        list_of_unsynced_caches: list = []

        for market in used_markets:
            if ubldc.is_depth_cache_synchronized(market=market) is True:
                list_of_synced_caches.append(market)
            else:
                list_of_unsynced_caches.append(market)

        add_string += f"\r\n found {len(list_of_synced_caches)} synced markets: {list_of_synced_caches}"
        add_string += f"\r\n found {len(list_of_unsynced_caches)} unsynced markets: {list_of_unsynced_caches}"
        ubldc.print_summary(add_string=add_string)

        time.sleep(1)


ubra = BinanceRestApiManager(exchange=exchange)
with BinanceLocalDepthCacheManager(exchange=exchange,
                                   ubra_manager=ubra,
                                   depth_cache_update_interval=update_interval_ms) as ubldc:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\r\nGracefully stopping ...")
    except Exception as e:
        print(f"\r\nERROR: {e}")
        print("Gracefully stopping ...")
