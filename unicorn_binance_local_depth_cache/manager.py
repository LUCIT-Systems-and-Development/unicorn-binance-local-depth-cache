#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_local_depth_cache/manager.py
#
# Part of ‘UNICORN Binance Local Depth Cache’
# Project website: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache
# Documentation: https://lucit-systems-and-development.github.io/unicorn-binance-local-depth-cache
# PyPI: https://pypi.org/project/unicorn-binance-local-depth-cache
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2022-2022, LUCIT Systems and Development (https://www.lucit.tech) and Oliver Zehentleitner
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from operator import itemgetter
from unicorn_binance_rest_api import *
from unicorn_binance_websocket_api import BinanceWebSocketApiManager
import logging
import time
import threading


logger = logging.getLogger("unicorn_binance_local_depth_cache")


class BinanceLocalDepthCacheManager(threading.Thread):
    def __init__(self, exchange="binance.com", ubwa_manager=False, default_refresh_interval=1800):
        """
        An unofficial Python API to use the Binance Websocket API`s (com+testnet, com-margin+testnet,
        com-isolated_margin+testnet, com-futures+testnet, us, jex, dex/chain+testnet) in a easy, fast, flexible,
        robust and fully-featured way.

        Binance API documentation:
        https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#how-to-manage-a-local-order-book-correctly

        :param exchange: Select binance.com, binance.com-testnet, binance.com-margin, binance.com-margin-testnet,
                         binance.com-isolated_margin, binance.com-isolated_margin-testnet, binance.com-futures,
                         binance.com-futures-testnet, binance.com-coin_futures, binance.us, trbinance.com,
                         jex.com, binance.org or binance.org-testnet (default: binance.com)
        :type exchange: str
        :param ubwa_manager: Provide a unicorn_binance_websocket_api.manager instance.
        :type ubwa_manager: BinanceWebSocketApiManager

        """
        super().__init__()
        self.version = "0.0.0.dev"
        self.exchange = exchange
        self.depth_caches = {}
        self.default_refresh_interval = default_refresh_interval
        self.timeout = 60
        self.ubra = BinanceRestApiManager("*", "*", exchange=self.exchange, disable_colorama=True)
        self.ubwa = ubwa_manager or BinanceWebSocketApiManager(exchange=self.exchange,
                                                               enable_stream_signal_buffer=True,
                                                               disable_colorama=True)
        self.stop_request = False
        self.thread_stream_signals = threading.Thread(target=self._process_stream_signals)
        self.thread_stream_signals.start()

    def _add_depth_cache(self, symbol=None, stream_id=None, refresh_interval=None):
        """
        Add a depth_cache to the depth_caches stack.

        :param symbol:
        :type symbol:
        :param stream_id:
        :type stream_id:

        :return: bool
        """
        if symbol:
            refresh_interval = refresh_interval or self.default_refresh_interval
            self.depth_caches[symbol.lower()] = {"asks": {},
                                                 "bids": {},
                                                 "last_refresh_time": None,
                                                 "last_update_id": None,
                                                 "last_update_time": None,
                                                 "refresh_interval": refresh_interval,
                                                 "stream_id": stream_id,
                                                 "symbol": symbol,
                                                 "thread": None}
            return True
        else:
            return False

    def _add_ask(self, ask, symbol: str = None):
        """
        Add an ask to a specific depth cache.

        :param ask:
        :type ask:
        :param symbol:
        :type symbol:
        :return: bool

        """
        self.depth_caches[symbol.lower()]["asks"][ask[0]] = float(ask[1])
        if ask[1] == "0.00000000":
            del self.depth_caches[symbol.lower()]["asks"][ask[0]]

    def _add_bid(self, bid, symbol: str = None):
        """
        Add a bid to a specific depth cache.

        :param bid:
        :type bid:
        :param symbol:
        :type symbol:
        :return: bool

        """
        self.depth_caches[symbol.lower()]["bids"][bid[0]] = float(bid[1])
        if bid[1] == "0.00000000":
            del self.depth_caches[symbol.lower()]["bids"][bid[0]]

    def _apply_updates(self, order_book, symbol: str = None):
        """
        Apply updates to a specific depth cache.

        :param order_book:
        :type order_book:
        :param symbol:
        :type symbol:
        :return:

        """
        for bid in order_book.get('b', []) + order_book.get('bids', []):
            self._add_bid(bid, symbol=symbol)
        for ask in order_book.get('a', []) + order_book.get('asks', []):
            self._add_ask(ask, symbol=symbol)
        self.update_time = order_book.get('E') or order_book.get('lastUpdateId')

    def _init_cache(self, symbol: str = None):
        """
        Initialise the depth cache with a rest snapshot.

        :param symbol:
        :type symbol:
        :return:
        """
        if self.ubwa.wait_till_stream_has_started(self.depth_caches[symbol.lower()]['stream_id']):
            logger.info(f"Check if stream {self.depth_caches[symbol.lower()]['stream_id']} with "
                        f"symbol {symbol} is running")
            time.sleep(0.5)
        logger.info(f"Init cache {symbol}")
        order_book = self.ubra.get_order_book(symbol=symbol, limit=1000)

        self.depth_caches[symbol.lower()]['asks'] = {}
        self.depth_caches[symbol.lower()]['bids'] = {}
        self.depth_caches[symbol.lower()]['last_refresh_time'] = int(time.time())
        self.depth_caches[symbol.lower()]['last_update_time'] = int(time.time())
        self.depth_caches[symbol.lower()]['last_update_id'] = int()

        # Process bids and asks from the order book
        self._apply_updates(order_book, symbol=symbol)
        for bid in order_book['bids']:
            self._add_bid(bid, symbol=symbol)
        for ask in order_book['asks']:
            self._add_ask(ask, symbol=symbol)

        # Set the first update id
        self.depth_caches[symbol.lower()]['last_update_id'] = int(order_book['lastUpdateId'])

        # Apply any updates from the stream_buffer
        stream_buffer_not_empty = True
        while stream_buffer_not_empty:
            stream_data = self.ubwa.pop_stream_data_from_stream_buffer(self.depth_caches[symbol.lower()]['stream_id'])
            if stream_data:
                self._process_stream_data(symbol=symbol)
            else:
                stream_buffer_not_empty = False

    def _process_stream_data(self, symbol: str = None):
        """
        Process depth stream_data

        :param symbol:
        :type symbol:
        :return:

        """
        logger.debug(f"Started thread for stream_data of symbol {symbol}")
        while self.stop_request is False:
            stream_data = self.ubwa.pop_stream_data_from_stream_buffer(self.depth_caches[symbol.lower()]['stream_id'])
            if stream_data:
                if self.depth_caches[symbol.lower()]['last_update_id'] is not None and \
                        int(stream_data['data']['u']) > self.depth_caches[symbol.lower()]['last_update_id']:
                    if stream_data['data']['U'] != self.depth_caches[symbol.lower()]['last_update_id'] + 1:
                        self._init_cache(symbol=symbol)
                    self._apply_updates(stream_data, symbol=symbol)
                    self.depth_caches[symbol.lower()]['last_update_id'] = stream_data['data']['u']
                    if self.depth_caches[symbol.lower()]['refresh_interval'] and \
                            int(time.time()) > self.depth_caches[symbol.lower()]['last_refresh_time']:
                        self._init_cache(symbol=symbol)
            time.sleep(0.02)

    def _process_stream_signals(self):
        logger.debug(f"Started thread for stream_signals")
        while self.stop_request is False:
            stream_signal = self.ubwa.pop_stream_signal_from_stream_signal_buffer()
            if stream_signal:
                logger.info(f"stream_signal: {stream_signal}")
            else:
                time.sleep(0.3)

    @staticmethod
    def _sort_depth(items, reverse=False):
        """
        Sort bids or asks by price

        :param items:
        :type items:
        :param reverse:
        :type reverse:
        :return: False or sorted list
        """
        if isinstance(items, dict):
            new_items = [[float(price), float(quantity)] for price, quantity in items.items()]
        elif isinstance(items, list):
            new_items = [[float(price), float(quantity)] for price, quantity in items]
        else:
            logger.critical(f"Unknown data type: {type(items)}")
            return False
        new_items = sorted(new_items, key=itemgetter(0), reverse=reverse)
        return new_items

    def create_depth_cache(self, symbol: str = None, update_speed: int = 1000, refresh_interval: int = None):
        """
        Create a new depth_cache!

        :param symbol: Symbol of the DepthCache
        :type symbol: str
        :param update_speed: Update speed of the depth webstream in milliseconds: 100 or 1000 (default)
        :type update_speed: int
        :param refresh_interval:
        :type refresh_interval: int
        :return: bool
        """
        if symbol is None:
            return False
        try:
            if self.depth_caches[symbol]:
                return False
        except KeyError as error_msg:
            logger.debug(f"No existing cache for symbol {symbol} found! - KeyError: {error_msg}")
        stream_id = self.ubwa.create_stream(f"depth@{update_speed}ms", symbol, stream_buffer_name=True, output="dict")
        self._add_depth_cache(symbol=symbol, stream_id=stream_id, refresh_interval=refresh_interval)
        self.depth_caches[symbol.lower()]['thread'] = threading.Thread(target=self._process_stream_data, args=(symbol,))
        self.depth_caches[symbol.lower()]['thread'].start()
        time.sleep(0.1)

    def get_bids(self, symbol: str = None):
        """
        Get the current bids

        :param symbol: Symbol of the DepthCache
        :type symbol: str
        :return: list of bids with price and quantity.

        """
        if symbol:
            return self._sort_depth(self.depth_caches[symbol.lower()]['bids'], reverse=True)
        else:
            raise ValueError(f"Missing parameter `symbol`")

    def get_asks(self, symbol: str = None):
        """
        Get the current asks

        :param symbol: Symbol of the DepthCache
        :type symbol: str
        :return: list of asks with price and quantity.

        """
        if symbol:
            return self._sort_depth(self.depth_caches[symbol.lower()]['bids'], reverse=False)
        else:
            raise ValueError(f"Missing parameter `symbol`")

    def reset_cache(self, symbol: str = None):
        """
        Reset the depth cache with a new rest snapshot.

        :param symbol:
        :type symbol:
        :return:
        """
        self._init_cache(symbol=symbol)
        return True
