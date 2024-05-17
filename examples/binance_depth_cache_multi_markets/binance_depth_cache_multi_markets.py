#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager
from typing import Optional
import asyncio
import logging
import os


amount_test_caches: int = 40
exchange: str = "binance.com"
update_interval_ms: Optional[int] = None

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def main():
    # We exclude some inactive markets:
    # https://www.binance.com/en/trade/BCC_USDT
    # https://www.binance.com/en/trade/VEN_USDT
    exclude_markets: list = ['BCCUSDT', 'TUSDUSDT', 'TRXUSDT', 'NULSUSDT', 'TUSDUSDT', 'PAXUSDT', 'BCHABCUSDT',
                             'BCHSVUSDT', 'BTTUSDT', 'USDSUSDT', 'USDCUSDT', 'TFUELUSDT', 'MITHUSDT', 'NANOUSDT',
                             'DASHUSDT', 'NEOUSDT', 'ICXUSDT', 'XMRUSDT', 'LINKUSDT', 'ONTUSDT', 'VENUSDT', 'FUNUSDT',
                             'WANUSDT', 'DOCKUSDT', 'STORMUSDT', 'MFTUSDT', 'PERLUSDT', 'COCOSUSDT', 'NPXSUSDT',
                             'USDSBUSDT', 'GTOUSDT', 'WINUSDT', 'CVCUSDT', 'TOMOUSDT', 'COSUSDT', 'ERDUSDT', 'BUSDUSDT',
                             'BEAMUSDT', 'HCUSDT', 'MCOUSDT', 'CTXCUSDT', 'ETCUSDT', 'XLMUSDT', 'QTUMUSDT', 'KNCUSDT',
                             'COMPUSDT', 'HNTUSDT', 'CTSIUSDT', 'AAVEUSDT']
    ubra = ubldc.get_ubra_manager()
    all_markets: list = [item['symbol'] for item in ubra.get_all_tickers() if item['symbol'].endswith("USDT")]
    markets: list = []

    for market in all_markets:
        if market not in exclude_markets:
            markets.append(market)
        if len(markets) >= amount_test_caches:
            break

    print(f"Starting {exchange} DepthCaches for {len(markets)} markets: {markets}")
    ubldc.create_depth_cache(markets=markets)

    while ubldc.is_stop_request() is False:
        markets_synced: list = []
        markets_not_synced: list = []
        for market in markets:
            if ubldc.is_depth_cache_synchronized(market=market) is True:
                markets_synced.append(market)
            else:
                markets_not_synced.append(market)
        add_string = (f"binance_api_status={ubra.get_used_weight(cached=True)}\r\n "
                      f"---------------------------------------------------------------------------------------------"
                      f"\r\n NOT SYNCED: {markets_not_synced}\r\n SYNCED: {markets_synced}")
        ubldc.print_summary(add_string=add_string)
        await asyncio.sleep(1)


with BinanceLocalDepthCacheManager(exchange=exchange,
                                   init_time_window=5,
                                   websocket_ping_interval=10,
                                   websocket_ping_timeout=20,
                                   depth_cache_update_interval=update_interval_ms) as ubldc:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\r\nGracefully stopping ...")
    except Exception as e:
        print(f"\r\nERROR: {e}")
        print("Gracefully stopping ...")
