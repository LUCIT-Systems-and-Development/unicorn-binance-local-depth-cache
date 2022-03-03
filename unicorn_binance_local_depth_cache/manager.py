#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_local_depth_cache/manager.py
#
# Part of ‘UNICORN Binance Local Depth Cache’
# Project website: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache
# Documentation: https://unicorn-binance-local-depth-cache.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-local-depth-cache
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2019-2022, LUCIT Systems and Development (https://www.lucit.tech) and Oliver Zehentleitner
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

# Todo:
#   - Control that last_update_id fits, if not, refresh!
#   - Refresh interval
#   - Test: multi caches
#   - Test: update works fine, cache data is fine?
#   - Test: Long run and find exceptions

from operator import itemgetter
from .exceptions import DepthCacheOutOfSync
from unicorn_binance_rest_api import BinanceRestApiManager
from unicorn_binance_websocket_api import BinanceWebSocketApiManager
import logging
import requests
import time
import threading


logger = logging.getLogger("unicorn_binance_local_depth_cache")


class BinanceLocalDepthCacheManager(threading.Thread):
    def __init__(self, exchange="binance.com", ubra_manager=False, ubwa_manager=False, default_refresh_interval=None,
                 warn_on_update=True):
        """
        A local Binance DepthCache for Python that supports multiple depth caches in one instance.

        Binance API documentation:
        https://developers.binance.com/docs/binance-api/spot-detail/web-socket-streams#diff-depth-stream

        :param exchange: Select binance.com, binance.com-testnet, binance.com-margin, binance.com-margin-testnet,
                         binance.com-isolated_margin, binance.com-isolated_margin-testnet, binance.com-futures,
                         binance.com-futures-testnet, binance.com-coin_futures, binance.us, trbinance.com,
                         jex.com, binance.org or binance.org-testnet (default: binance.com)
        :type exchange: str
        :param ubra_manager: Provide a shared unicorn_binance_rest_api.manager instance
        :type ubra_manager: BinanceRestApiManager
        :param ubwa_manager: Provide a shared unicorn_binance_websocket_api.manager instance
        :type ubwa_manager: BinanceWebSocketApiManager
        :param default_refresh_interval: The default refresh interval in seconds, default is None.
        :type default_refresh_interval: int
        :param warn_on_update: set to `False` to disable the update warning
        :type warn_on_update: bool
        """
        super().__init__()
        self.version = "0.1.0.dev"
        self.exchange = exchange
        logger.info(f"New instance of {self.name} for exchange {exchange} started ...")
        self.depth_caches = {}
        self.default_refresh_interval = default_refresh_interval
        self.last_update_check_github = {'timestamp': time.time(),
                                         'status': None}
        self.name = "unicorn-binance-local-depth-cache"
        self.timeout = 60
        self.ubra = ubra_manager or BinanceRestApiManager("*", "*", exchange=self.exchange, disable_colorama=True)
        self.ubwa = ubwa_manager or BinanceWebSocketApiManager(exchange=self.exchange,
                                                               enable_stream_signal_buffer=True,
                                                               disable_colorama=True)
        self.stop_request = False
        if warn_on_update and self.is_update_available():
            update_msg = f"Release {self.name}_" + self.get_latest_version() + " is available, " \
                         "please consider updating! (Changelog: https://github.com/LUCIT-Systems-and-Development/" \
                         "unicorn-binance-local-depth-cache/blob/master/CHANGELOG.md)"
            print(update_msg)
            logger.warning(update_msg)
        self.thread_stream_signals = threading.Thread(target=self._process_stream_signals)
        self.thread_stream_signals.start()

    def _add_depth_cache(self, symbol=None, stream_id=None, refresh_interval=None):
        """
        Add a depth_cache to the depth_caches stack.

        :param symbol: Specify the market symbol for the used depth_cache
        :type symbol: str
        :param stream_id: Provide a stream_id
        :type stream_id: str
        :return: bool
        """
        if symbol and stream_id:
            self.depth_caches[symbol.lower()] = {"asks": {},
                                                 "bids": {},
                                                 "is_synchronized": False,
                                                 "last_refresh_time": None,
                                                 "last_update_id": None,
                                                 "refresh_interval": refresh_interval or self.default_refresh_interval,
                                                 "refresh_request": False,
                                                 "stop_request": False,
                                                 "stream_id": stream_id,
                                                 "stream_status": None,
                                                 "symbol": symbol,
                                                 "thread": None,
                                                 "thread_is_started": False}
            logger.debug(f"_add_depth_cache() - Added new entry for symbol {symbol} and stream_id {stream_id}")
            return True
        else:
            logger.debug(f"_add_depth_cache() - Not able to add entry for symbol {symbol} and stream_id {stream_id}")
            return False

    def _add_ask(self, ask, symbol: str = None):
        """
        Add an ask to a specific depth cache.

        :param ask: Add asks to the depth_cache
        :type ask: list
        :param symbol: Specify the market symbol for the used depth_cache
        :type symbol: str
        :return: bool
        """
        self.depth_caches[symbol.lower()]["asks"][ask[0]] = float(ask[1])
        if ask[1] == "0.00000000":
            logger.debug(f"_add_ask() - Deleting depth position {self.depth_caches[symbol.lower()]['asks'][ask[0]]} "
                         f"on ask side")
            del self.depth_caches[symbol.lower()]["asks"][ask[0]]
        return True

    def _add_bid(self, bid, symbol: str = None):
        """
        Add a bid to a specific depth cache.

        :param bid: Add bids to the depth_cache
        :type bid: list
        :param symbol: Specify the market symbol for the used depth_cache
        :type symbol: str
        :return: bool
        """
        self.depth_caches[symbol.lower()]["bids"][bid[0]] = float(bid[1])
        if bid[1] == "0.00000000":
            logger.debug(f"_add_bid() - Deleting depth position {self.depth_caches[symbol.lower()]['bids'][bid[0]]} "
                         f"on bid side")
            del self.depth_caches[symbol.lower()]["bids"][bid[0]]
        return True

    def _apply_updates(self, order_book, symbol: str = None):
        """
        Apply updates to a specific depth cache.

        :param order_book: Provide order_book data from rest or ws
        :type order_book: dict
        :param symbol: Specify the market symbol for the used depth_cache
        :type symbol: str
        :return: bool
        """
        logger.debug(f"_apply_updates() - Applying updates to the depth cache with symbol {symbol}")
        for ask in order_book.get('a', []) + order_book.get('asks', []):
            self._add_ask(ask, symbol=symbol)
        for bid in order_book.get('b', []) + order_book.get('bids', []):
            self._add_bid(bid, symbol=symbol)
        return True

    def _init_depth_cache(self, symbol: str = None):
        """
        Initialise the depth cache with a rest snapshot.

        :param symbol: Specify the market symbol for the used depth_cache
        :type symbol: str
        :return: bool
        """
        logger.info(f"_init_depth_cache() - Starting initialization of the cache with symbol {symbol}")
        order_book = self.ubra.get_order_book(symbol=symbol, limit=1000)
        logger.debug(f"_init_depth_cache() - Downloaded order_book snapshot for the depth cache with symbol {symbol}")
        self.depth_caches[symbol.lower()]['asks'] = {}
        self.depth_caches[symbol.lower()]['bids'] = {}
        self.depth_caches[symbol.lower()]['last_refresh_time'] = int(time.time())
        self.depth_caches[symbol.lower()]['last_update_time'] = int(time.time())
        self.depth_caches[symbol.lower()]['last_update_id'] = int(order_book['lastUpdateId'])
        self._apply_updates(order_book, symbol=symbol)
        for bid in order_book['bids']:
            self._add_bid(bid, symbol=symbol)
        for ask in order_book['asks']:
            self._add_ask(ask, symbol=symbol)
        logger.debug(f"_init_depth_cache() - Finished initialization of the cache with symbol {symbol}")
        return True

    def _process_stream_data(self, symbol: str = None):
        """
        Process depth stream_data

        The logic is described here:
        https://developers.binance.com/docs/binance-api/spot-detail/web-socket-streams#how-to-manage-a-local-order-book-correctly

        :param symbol: Specify the market symbol for the used depth_cache
        :type symbol: str
        """
        logger.debug(f"_process_stream_data() - Started thread for stream_data of symbol {symbol}")
        self.depth_caches[symbol.lower()]['thread_is_started'] = True
        self.depth_caches[symbol.lower()]['is_synchronized'] = False
        while self.stop_request is False and self.depth_caches[symbol.lower()]['stop_request'] is False:
            logger.info(f"_process_stream_data() - Clearing stream_buffer with stream_id "
                        f"{self.depth_caches[symbol.lower()]['stream_id']} of the "
                        f"cache of symbol {symbol} (stream_buffer length: "
                        f"{self.ubwa.get_stream_buffer_length(self.depth_caches[symbol.lower()]['stream_id'])}")
            self.depth_caches[symbol.lower()]['refresh_request'] = False
            self.ubwa.clear_stream_buffer(self.depth_caches[symbol.lower()]['stream_id'])
            logger.info(f"_process_stream_data() - Cleared stream_buffer: "
                        f"{self.ubwa.get_stream_buffer_length(self.depth_caches[symbol.lower()]['stream_id'])} items")
            while self.ubwa.get_stream_buffer_length(self.depth_caches[symbol.lower()]['stream_id']) < 3:
                logger.debug(f"_process_stream_data() - Waiting for enough depth events for depth_cache with "
                             f"symbol {symbol}")
                time.sleep(0.01)
            logger.info(f"_process_stream_data() - Collected enough depth events, starting the initialization of the "
                        f"cache with symbol {symbol}")
            self._init_depth_cache(symbol=symbol)
            while self.stop_request is False and self.depth_caches[symbol.lower()]['stop_request'] is False:
                if self.depth_caches[symbol.lower()]['refresh_request'] is True:
                    break
                stream_data = self.ubwa.pop_stream_data_from_stream_buffer(self.depth_caches[symbol.lower()]['stream_id'])
                if stream_data and "'result': None," not in str(stream_data):
                    if self.depth_caches[symbol.lower()]['is_synchronized'] is False:
                        if int(stream_data['data']['u']) <= self.depth_caches[symbol.lower()]['last_update_id']:
                            # Drop it
                            logger.info(f"_process_stream_data() - Dropping outdated depth update of the cache with "
                                        f"symbol {symbol}")
                            continue
                        if int(stream_data['data']['U']) <= self.depth_caches[symbol.lower()]['last_update_id'] \
                                <= int(stream_data['data']['u']):
                            # This is the first applied depth update
                            self._apply_updates(stream_data, symbol=symbol)
                            logger.info(f"_process_stream_data() - Finished initialization of the cache with "
                                        f"symbol {symbol}")
                            self.depth_caches[symbol.lower()]['is_synchronized'] = True
                        self.depth_caches[symbol.lower()]['last_update_id'] = stream_data['data']['u']
                    else:
                        # Regular depth update events
                        logger.debug(f"_process_stream_data() - Applying regular depth update to the depth cache with "
                                     f"symbol {symbol}")
                        # Todo: While listening to the stream, each new event's U should be equal to the previous
                        #  event's u+1. If not -> new init
                        self._apply_updates(stream_data, symbol=symbol)
                time.sleep(0.01)

    def _process_stream_signals(self):
        """
        Process stream_signals
        """
        logger.debug(f"_process_stream_signals() - Started thread for stream_signals")
        while self.stop_request is False:
            stream_signal = self.ubwa.pop_stream_signal_from_stream_signal_buffer()
            if stream_signal:
                logger.debug(f"_process_stream_signals() - received stream_signal: {stream_signal}")
                for symbol in self.depth_caches:
                    if self.depth_caches[symbol]['stream_id'] == stream_signal['stream_id']:
                        self.depth_caches[symbol]['stream_status'] = stream_signal['type']
                        if stream_signal['type'] == "DISCONNECT":
                            self.depth_caches[symbol]['is_synchronized'] = False
                            self.depth_caches[symbol]['refresh_request'] = True
            else:
                time.sleep(0.01)

    @staticmethod
    def _sort_depth_cache(items, reverse=False):
        """
        Sort asks or bids by price

        :param items: asks or bids
        :type items: dict
        :param reverse: False is regular, True is reversed
        :type reverse: bool
        :return: False or sorted list
        """
        logger.debug(f"_sort_depth_cache() - Start sorting")
        new_items = [[float(price), float(quantity)] for price, quantity in items.items()]
        new_items = sorted(new_items, key=itemgetter(0), reverse=reverse)
        return new_items

    def create_depth_cache(self, symbol: str = None, update_speed: int = 1000, refresh_interval: int = None):
        """
        Create a new depth_cache!

        :param symbol: Specify the market symbol for the used depth_cache
        :type symbol: str
        :param update_speed: Update speed of the depth webstream in milliseconds: 100 or 1000 (default) - based on
                             https://developers.binance.com/docs/binance-api/spot-detail/web-socket-streams#diff-depth-stream
        :type update_speed: int
        :param refresh_interval: The refresh interval in seconds, default is the `default_refresh_interval`.
        :type refresh_interval: int
        :return: bool
        """
        if symbol is None:
            return False
        try:
            if self.depth_caches[symbol]:
                logger.debug(f"create_depth_cache() - depth_cache {symbol} already exists!")
                return False
        except KeyError as error_msg:
            logger.debug(f"create_depth_cache() - No existing cache for symbol {symbol} found! - KeyError: {error_msg}")
        stream_id = self.ubwa.create_stream(f"depth@{update_speed}ms", symbol, stream_buffer_name=True, output="dict")
        self._add_depth_cache(symbol=symbol, stream_id=stream_id, refresh_interval=refresh_interval)
        self.depth_caches[symbol.lower()]['thread'] = threading.Thread(target=self._process_stream_data, args=(symbol,))
        self.depth_caches[symbol.lower()]['thread'].start()
        while self.depth_caches[symbol.lower()]['thread_is_started'] is False:
            # This is to await the creation of the thread to avoid errors if the main thread gets closed before. This
            # can happen if after calling `create_depth_cache()` the main thread has no more code and exits.
            logger.debug(f"create_depth_cache() - Waiting till thread for symbol {symbol} is running")
            time.sleep(0.01)
        return True

    def get_asks(self, symbol: str = None):
        """
        Get the current asks

        :param symbol: Specify the market symbol for the used depth_cache
        :type symbol: str
        :return: list of asks with price and quantity.
        """
        if self.depth_caches[symbol.lower()]['is_synchronized'] is False:
            try:
                raise DepthCacheOutOfSync(f"The depth cache for market symbol '{symbol}' is out of sync, please try "
                                          f"again later")
            except KeyError:
                raise KeyError(f"Invalid value provided: symbol={symbol}")

        if symbol:
            return self._sort_depth_cache(self.depth_caches[symbol.lower()]['asks'], reverse=True)
        else:
            raise KeyError(f"Missing parameter `symbol`")

    def get_bids(self, symbol: str = None):
        """
        Get the current bids

        :param symbol: Specify the market symbol for the used depth_cache
        :type symbol: str
        :return: list of asks with price and quantity.
        """
        try:
            if self.depth_caches[symbol.lower()]['is_synchronized'] is False:
                raise DepthCacheOutOfSync(f"The depth cache for market symbol '{symbol}' is out of sync, please try "
                                          f"again later")
        except KeyError:
            raise KeyError(f"Invalid value provided: symbol={symbol}")
        if symbol:
            return self._sort_depth_cache(self.depth_caches[symbol.lower()]['bids'], reverse=False)
        else:
            raise KeyError(f"Missing parameter `symbol`")

    @staticmethod
    def get_latest_release_info():
        """
        Get info about the latest available release

        :return: dict or False
        """
        logger.debug(f"get_latest_release_info() - Starting the request")
        try:
            respond = requests.get('https://api.github.com/repos/LUCIT-Systems-and-Development/'
                                   'unicorn-binance-local-depth-cache/releases/latest')
            latest_release_info = respond.json()
            return latest_release_info
        except Exception:
            return False

    def get_latest_version(self):
        """
        Get the version of the latest available release (cache time 1 hour)

        :return: str or False
        """
        logger.debug(f"get_latest_version() - Starting the request")
        # Do a fresh request if status is None or last timestamp is older 1 hour
        if self.last_update_check_github['status'] is None or \
                (self.last_update_check_github['timestamp'] + (60 * 60) < time.time()):
            self.last_update_check_github['status'] = self.get_latest_release_info()
        if self.last_update_check_github['status']:
            try:
                return self.last_update_check_github['status']["tag_name"]
            except KeyError:
                return "unknown"
        else:
            return "unknown"

    def get_version(self):
        """
        Get the package/module version

        :return: str
        """
        return self.version

    def is_update_available(self):
        """
        Is a new release of this package available?

        :return: bool
        """
        logger.debug(f"is_update_available() - Starting the request")
        installed_version = self.get_version()
        if ".dev" in installed_version:
            installed_version = installed_version[:-4]
        if self.get_latest_version() == installed_version:
            return False
        elif self.get_latest_version() == "unknown":
            return False
        else:
            return True

    def stop_manager(self):
        """
        Stop unicorn-binance-local-depth-cache with all sub routines

        :return: bool
        """
        logger.debug(f"stop_manager() - Stop initiated")
        self.stop_request = True
        self.ubwa.stop_manager_with_all_streams()
        return True
