#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

from unicorn_binance_websocket_api import *
from unicorn_binance_rest_api import *
import asyncio
import logging
import os

exchange = "binance.com-futures"

logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


async def main(ubra: BinanceRestApiManager = None, ubwa: BinanceWebSocketApiManager = None):
    async def process_asyncio_queue(stream_id=None):
        print(f"Start processing the data from stream '{ubwa.get_stream_label(stream_id)}':")
        while ubwa.is_stop_request(stream_id) is False:
            data = await ubwa.get_stream_data_from_asyncio_queue(stream_id)
            print(data)
            ubwa.asyncio_queue_task_done(stream_id)

    markets = ['TRXUSDT']

    stream_id = ubwa.create_stream(channels=['depth'],
                                   markets=markets,
                                   stream_label="Depth Diff",
                                   process_asyncio_queue=process_asyncio_queue)
    print(f"Subscribed to: {ubwa.get_stream_info(stream_id=stream_id)['markets']}")
    while not ubwa.is_manager_stopping():
        #ubwa.print_summary()
        print(f"INFO: {ubwa.get_stream_info(stream_id=stream_id)['markets']}")
        await asyncio.sleep(1)


ubra_manager = BinanceRestApiManager(exchange=exchange)
with BinanceWebSocketApiManager(exchange=exchange) as ubwa_manager:
    try:
        asyncio.run(main(ubra=ubra_manager, ubwa=ubwa_manager))
    except KeyboardInterrupt:
        print("\r\nGracefully stopping ...")
    except Exception as e:
        print(f"\r\nERROR: {e}\r\nGracefully stopping ...")
ubra_manager.stop_manager()
