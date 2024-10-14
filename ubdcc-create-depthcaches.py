#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheClusterNotReachableError
from unicorn_binance_rest_api import BinanceRestApiManager
import asyncio
import logging
import os

exchange: str = "binance.com-futures"
ubdcc_address = ""
exclude: list = ['TUSDUSDT', 'ONGUSDT', 'TFUELUSDT', 'WINUSDT', 'WANUSDT', 'FUNUSDT', 'CVCUSDT', 'ARPAUSDT', 'CTXCUSDT',
                 'TROYUSDT', 'VITEUSDT', 'FTTUSDT', 'EURUSDT', 'WRXUSDT', 'LTOUSDT', 'MBLUSDT', 'STPTUSDT', 'DATAUSDT',
                 'CTSIUSDT', 'HIVEUSDT', 'ARDRUSDT', 'MDTUSDT', 'SCUSDT', 'VTHOUSDT', 'DGBUSDT', 'DCRUSDT', 'IRISUSDT',
                 'KMDUSDT', 'JSTUSDT', 'LUNAUSDT', 'PAXGUSDT', 'WINGUSDT', 'ORNUSDT', 'UTKUSDT', 'AUDIOUSDT', 'CTKUSDT',
                 'AKROUSDT', 'HARDUSDT', 'STRAXUSDT', 'AVAUSDT', 'JUVUSDT', 'PSGUSDT', 'OGUSDT', 'ATMUSDT', 'ASRUSDT',
                 'FIROUSDT', 'DODOUSDT', 'ACMUSDT', 'FISUSDT', 'PONDUSDT', 'DEGOUSDT', 'TKOUSDT', 'PUNDIXUSDT',
                 'BARUSDT', 'FORTHUSDT', 'BURGERUSDT', 'SLPUSDT', 'SHIBUSDT', 'ERNUSDT', 'PHAUSDT', 'MLNUSDT',
                 'DEXEUSDT', 'CLVUSDT', 'RAYUSDT', 'FARMUSDT', 'QUICKUSDT', 'REQUSDT', 'GNOUSDT', 'XECUSDT',
                 'ELFUSDT', 'IDEXUSDT', 'USDPUSDT', 'DFUSDT', 'RADUSDT', 'BETAUSDT', 'LAZIOUSDT', 'ADXUSDT',
                 'CITYUSDT', 'KP3RUSDT', 'QIUSDT', 'PORTOUSDT', 'AMPUSDT', 'PYRUSDT', 'ALCXUSDT', 'SANTOSUSDT',
                 'WAXPUSDT', 'CVXUSDT', 'OOKIUSDT', 'GLMRUSDT', 'SCRTUSDT', 'BTTCUSDT', 'ACAUSDT', 'XNOUSDT',
                 'ALPINEUSDT', 'AUCTIONUSDT', 'BIFIUSDT', 'NEXOUSDT', 'LUNCUSDT', 'OSMOUSDT', 'PROSUSDT', 'GNSUSDT',
                 'VIBUSDT', 'PROMUSDT', 'QKCUSDT', 'UFTUSDT', 'OAXUSDT', 'WBTCUSDT', 'PEPEUSDT', 'FLOKIUSDT',
                 'ASTUSDT', 'SNTUSDT', 'WBETHUSDT', 'FDUSDUSDT', 'CREAMUSDT', 'GFTUSDT', 'IQUSDT', 'PIVXUSDT',
                 'VICUSDT', 'LPTUSDT', 'AEURUSDT', 'BONKUSDT']

logging.getLogger("unicorn_binance_local_depth_cache")
logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def main():
    with BinanceRestApiManager(exchange=exchange) as ubra:
        exchange_info = ubra.get_exchange_info()
        markets = []
        for item in exchange_info['symbols']:
            if item['symbol'].endswith("USDT") and item['status'] == "TRADING" and item['symbol'] not in exclude:
                markets.append(item['symbol'])
    markets = markets[:200]
    print(f"Adding {len(markets)} DepthCaches for exchange '{exchange}' on UBDCC '{ubdcc_address}'!")
    loop = 1
    for market in markets:
        print(f"Creating DepthCache #{loop}: {market}")
        ubldc.create_depth_cache(markets=market, desired_quantity=2)
        loop += 1
        await asyncio.sleep(2.25)

try:
    with BinanceLocalDepthCacheManager(exchange=exchange, ubdcc_address=ubdcc_address) as ubldc:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\r\nGracefully stopping ...")
except DepthCacheClusterNotReachableError as error_msg:
    print(f"ERROR: {error_msg}")
