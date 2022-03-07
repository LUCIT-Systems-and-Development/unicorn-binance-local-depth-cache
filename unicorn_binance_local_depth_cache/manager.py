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

from .exceptions import DepthCacheOutOfSync
from operator import itemgetter
from unicorn_binance_rest_api import BinanceRestApiManager
from unicorn_binance_websocket_api import BinanceWebSocketApiManager
from typing import Optional, Union
import logging
import platform
import requests
import time
import threading


logger = logging.getLogger("unicorn_binance_local_depth_cache")


class BinanceLocalDepthCacheManager(threading.Thread):
    """
     A local Binance DepthCache Manager for Python that supports multiple depth caches in one instance in a easy, fast,
     flexible, robust and fully-featured way.

     Binance API documentation:
     https://developers.binance.com/docs/binance-api/spot-detail/web-socket-streams#diff-depth-stream
     https://binance-docs.github.io/apidocs/futures/en/#diff-book-depth-streams

     :param exchange: Select binance.com, binance.com-testnet, binance.com-margin, binance.com-margin-testnet,
                      binance.com-isolated_margin, binance.com-isolated_margin-testnet, binance.com-futures,
                      binance.com-futures-testnet, binance.com-coin_futures, binance.us, trbinance.com,
                      jex.com, binance.org or binance.org-testnet (default: binance.com)
     :type exchange: str
     :param default_refresh_interval: The default refresh interval in seconds, default is None.
     :type default_refresh_interval: int
     :param default_update_interval: Update speed of the depth webstream in milliseconds. More info:
                                     https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/wiki/update_intervals
                                     This can be overwritten with `update_interval` of `create_depth_cache()`.
     :type default_update_interval: int
     :param warn_on_update: set to `False` to disable the update warning
     :type warn_on_update: bool
     :param ubra_manager: Provide a shared unicorn_binance_rest_api.manager instance
     :type ubra_manager: BinanceRestApiManager
     :param ubwa_manager: Provide a shared unicorn_binance_websocket_api.manager instance. Use
                          `enable_stream_signal_buffer=True <https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api.html?highlight=enable_stream_signal_buffer%20true#module-unicorn_binance_websocket_api.manager>`_
                          otherwise the depth_cache will not work as it should!
     :type ubwa_manager: BinanceWebSocketApiManager
     """

    def __init__(self, exchange: str = "binance.com",
                 default_refresh_interval: Optional[int] = None,
                 default_update_interval: Optional[int] = None,
                 warn_on_update: bool = True,
                 ubra_manager: Optional[Union[BinanceRestApiManager, bool]] = False,
                 ubwa_manager: Optional[Union[BinanceWebSocketApiManager, bool]] = False):
        super().__init__()
        self.version = "0.5.2"
        self.name = "unicorn-binance-local-depth-cache"
        logger.info(f"New instance of {self.name} on "
                    f"{str(platform.system())} {str(platform.release())} for exchange {exchange} started ...")
        self.exchange = exchange
        self.depth_caches = {}
        self.default_update_interval = default_update_interval
        self.default_refresh_interval = default_refresh_interval
        self.last_update_check_github = {'timestamp': time.time(),
                                         'status': None}
        self.timeout = 60
        try:
            self.ubra = ubra_manager or BinanceRestApiManager("*", "*", exchange=self.exchange, disable_colorama=True)
        except requests.exceptions.ConnectionError as error_msg:
            error_msg = f"Can not initialize BinanceLocalDepthCacheManager() - No internet connection? - {error_msg}"
            logger.critical(error_msg)
            raise ConnectionRefusedError(error_msg)
        if ubwa_manager:
            if not ubwa_manager.is_stream_signal_buffer_enabled():
                error_msg = f"The shared `ubwa_manager` must use `enable_stream_signal_buffer=True` otherwise the " \
                            f"depth_cache will not work as it should! \r\n More info: " \
                            f"https://unicorn-binance-websocket-api.docs.lucit.tech/unicorn_binance_websocket_api." \
                            f"html?highlight=enable_stream_signal_buffer%20true#module-unicorn_binance_websocket_api" \
                            f".manager"
                logger.critical(error_msg)
                raise RuntimeWarning(error_msg)
        self.ubwa = ubwa_manager or BinanceWebSocketApiManager(exchange=self.exchange,
                                                               enable_stream_signal_buffer=True,
                                                               disable_colorama=True)
        self.stop_request = False
        self.threading_lock_ask = {}
        self.threading_lock_bid = {}
        if warn_on_update and self.is_update_available():
            update_msg = f"Release {self.name}_" + self.get_latest_version() + " is available, " \
                         "please consider updating! (Changelog: https://github.com/LUCIT-Systems-and-Development/" \
                         "unicorn-binance-local-depth-cache/blob/master/CHANGELOG.md)"
            print(update_msg)
            logger.warning(update_msg)
        self.thread_stream_signals = threading.Thread(target=self._process_stream_signals)
        self.thread_stream_signals.start()

    def _add_depth_cache(self, market=None, stream_id=None, refresh_interval=None):
        """
        Add a depth_cache to the depth_caches stack.

        :param market: Specify the market market for the used depth_cache
        :type market: str
        :param stream_id: Provide a stream_id
        :type stream_id: str
        :return: bool
        """
        if market and stream_id:
            self.depth_caches[market.lower()] = {'asks': {},
                                                 'bids': {},
                                                 'is_synchronized': False,
                                                 'last_refresh_time': None,
                                                 'last_update_id': None,
                                                 'refresh_interval': refresh_interval or self.default_refresh_interval,
                                                 'refresh_request': False,
                                                 'stop_request': False,
                                                 'stream_id': stream_id,
                                                 'stream_status': None,
                                                 'market': market.lower(),
                                                 'thread': None,
                                                 'thread_is_started': False}
            self.threading_lock_ask[market.lower()] = threading.Lock()
            self.threading_lock_bid[market.lower()] = threading.Lock()
            logger.debug(f"BinanceLocalDepthCacheManager._add_depth_cache() - Added new entry for market"
                         f" {market.lower()} and stream_id {stream_id}")
            return True
        else:
            logger.debug(f"BinanceLocalDepthCacheManager._add_depth_cache() - Not able to add entry for market"
                         f" {market} and stream_id {stream_id}")
            return False

    def _add_ask(self, ask, market: str = None):
        """
        Add, update or delete an ask of a specific depth_cache.

        :param ask: Add asks to the depth_cache
        :type ask: list
        :param market: Specify the market market for the used depth_cache
        :type market: str
        :return: bool
        """
        with self.threading_lock_ask[market.lower()]:
            self.depth_caches[market.lower()]['asks'][ask[0]] = float(ask[1])
            if ask[1] == "0.00000000" or ask[1] == "0.000":
                logger.debug(f"BinanceLocalDepthCacheManager._add_ask() - Deleting depth position {ask[0]} on ask "
                             f"side for market {market.lower()}")
                del self.depth_caches[market.lower()]['asks'][ask[0]]
            return True

    def _add_bid(self, bid, market: str = None):
        """
        Add a bid to a specific depth_cache.

        :param bid: Add bids to the depth_cache
        :type bid: list
        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :return: bool
        """
        with self.threading_lock_bid[market.lower()]:
            self.depth_caches[market.lower()]['bids'][bid[0]] = float(bid[1])
            if bid[1] == "0.00000000" or bid[1] == "0.000":
                logger.debug(f"BinanceLocalDepthCacheManager._add_bid() - Deleting depth position {bid[0]} on bid "
                             f"side for market {market.lower()}")
                del self.depth_caches[market.lower()]['bids'][bid[0]]
            return True

    def _apply_updates(self, order_book, market: str = None):
        """
        Apply updates to a specific depth_cache

        :param order_book: Provide order_book data from rest or ws
        :type order_book: dict
        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :return: bool
        """
        logger.debug(f"BinanceLocalDepthCacheManager._apply_updates() - Applying updates to the depth_cache with "
                     f"market {market.lower()}")
        for ask in order_book.get('a', []) + order_book.get('asks', []):
            self._add_ask(ask, market=market.lower())
        for bid in order_book.get('b', []) + order_book.get('bids', []):
            self._add_bid(bid, market=market.lower())
        return True

    def _get_order_book_from_depth_cache(self, market: str = None):
        """
        Get the order_book of the chosen market.

        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :return: order_book or False
        """
        try:
            if self.exchange == "binance.com" or self.exchange == "binance.com-testnet":
                order_book = self.ubra.get_order_book(symbol=market.upper(), limit=1000)
            elif self.exchange == "binance.com-futures":
                order_book = self.ubra.futures_order_book(symbol=market.upper(), limit=1000)
            else:
                return False
        except requests.exceptions.ConnectionError as error_msg:
            logger.error(f"BinanceLocalDepthCacheManager._init_depth_cache() - Can not download order_book snapshot "
                         f"for the depth_cache with market {market.lower()} -> trying again till it works - "
                         f"error_msg: {error_msg}")

            return False
        except requests.exceptions.ReadTimeout as error_msg:
            logger.error(f"BinanceLocalDepthCacheManager._init_depth_cache() - Can not download order_book snapshot "
                         f"for the depth_cache with market {market.lower()} -> trying again till it works - "
                         f"error_msg: {error_msg}")
            return False
        logger.debug(f"BinanceLocalDepthCacheManager._init_depth_cache() - Downloaded order_book snapshot for "
                     f"the depth_cache with market {market.lower()}")
        return order_book

    def _init_depth_cache(self, market: str = None):
        """
        Initialise the depth_cache with a rest snapshot.

        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :return: bool
        """
        logger.info(f"BinanceLocalDepthCacheManager._init_depth_cache() - Starting initialization of the cache "
                    f"with market {market.lower()}")
        order_book = self._get_order_book_from_depth_cache(market=market.lower())
        if order_book is False:
            return False
        self._reset_depth_cache(market=market.lower())
        self.depth_caches[market.lower()]['last_refresh_time'] = int(time.time())
        self.depth_caches[market.lower()]['last_update_time'] = int(time.time())
        self.depth_caches[market.lower()]['last_update_id'] = int(order_book['lastUpdateId'])
        self._apply_updates(order_book, market=market.lower())
        for bid in order_book['bids']:
            self._add_bid(bid, market=market.lower())
        for ask in order_book['asks']:
            self._add_ask(ask, market=market.lower())
        logger.debug(f"BinanceLocalDepthCacheManager._init_depth_cache() - Finished initialization of the cache "
                     f"with market {market.lower()}")
        return True

    def _process_stream_data(self, market: str = None):
        """
        Process depth stream_data

        The logic is described here:
        - Binance Spot: https://developers.binance.com/docs/binance-api/spot-detail/web-socket-streams#how-to-manage-a-local-order-book-correctly
        - Binance Futures: https://binance-docs.github.io/apidocs/futures/en/#diff-book-depth-streams

        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        """
        logger.debug(f"BinanceLocalDepthCacheManager._process_stream_data() - Started thread for stream_data of "
                     f"market {market.lower()}")
        self.depth_caches[market.lower()]['thread_is_started'] = True
        while self.is_stop_request(market=market.lower()) is False:
            logger.info(f"BinanceLocalDepthCacheManager._process_stream_data() - Clearing stream_buffer with stream_id "
                        f"{self.depth_caches[market.lower()]['stream_id']} of the "
                        f"cache of market {market.lower()} (stream_buffer length: "
                        f"{self.ubwa.get_stream_buffer_length(self.depth_caches[market.lower()]['stream_id'])}")
            self.depth_caches[market.lower()]['is_synchronized'] = False
            self.depth_caches[market.lower()]['refresh_request'] = False
            self.ubwa.clear_stream_buffer(self.depth_caches[market.lower()]['stream_id'])
            logger.info(f"BinanceLocalDepthCacheManager._process_stream_data() - Cleared stream_buffer: "
                        f"{self.ubwa.get_stream_buffer_length(self.depth_caches[market.lower()]['stream_id'])} items")
            while self.ubwa.get_stream_buffer_length(self.depth_caches[market.lower()]['stream_id']) <= 2 and \
                    self.is_stop_request(market=market.lower()) is False:
                logger.debug(f"BinanceLocalDepthCacheManager._process_stream_data() - Waiting for enough depth "
                             f"events for depth_cache with market {market.lower()}")
                time.sleep(0.1)
            logger.info(f"BinanceLocalDepthCacheManager._process_stream_data() - Collected enough depth events, "
                        f"starting the initialization of the cache with market {market.lower()}")
            if not self._init_depth_cache(market=market.lower()):
                logger.info(f"BinanceLocalDepthCacheManager._process_stream_data() - Not able to initiate depth_cache "
                            f"with market {market.lower()}")
                continue
            while self.is_stop_request(market=market.lower()) is False:
                if self.depth_caches[market.lower()]['refresh_request'] is True:
                    self.depth_caches[market.lower()]['is_synchronized'] = False
                    logger.info(f"BinanceLocalDepthCacheManager._process_stream_data() - Catched refresh_request "
                                f"for depth_cache with market {market.lower()} - lets try again")
                    break
                stream_data = self.ubwa.pop_stream_data_from_stream_buffer(self.depth_caches[market.lower()]['stream_id'])
                if stream_data and "'result': None" not in str(stream_data):
                    if self.depth_caches[market.lower()]['is_synchronized'] is False:
                        if self.exchange == "binance.com" or self.exchange == "binance.com-testnet":
                            if int(stream_data['data']['u']) <= self.depth_caches[market.lower()]['last_update_id']:
                                # Drop it
                                logger.info(f"BinanceLocalDepthCacheManager._process_stream_data() - Dropping "
                                            f"outdated depth update of the cache with market {market.lower()}")
                                continue
                            if int(stream_data['data']['U']) <= self.depth_caches[market.lower()]['last_update_id']+1 \
                                    <= int(stream_data['data']['u']):
                                # The first processed event should have U <= lastUpdateId+1 AND u >= lastUpdateId+1.
                                self._apply_updates(stream_data['data'], market=market.lower())
                                logger.info(f"BinanceLocalDepthCacheManager._process_stream_data() - Finished "
                                            f"initialization of the cache with market {market.lower()}")
                                # Init (refresh) finished
                                self.depth_caches[market.lower()]['is_synchronized'] = True
                                self.depth_caches[market.lower()]['last_refresh_time'] = int(time.time())
                        elif self.exchange == "binance.com-futures":
                            if int(stream_data['data']['u']) < self.depth_caches[market.lower()]['last_update_id']:
                                # Drop it
                                logger.info(f"BinanceLocalDepthCacheManager._process_stream_data() - Dropping "
                                            f"outdated depth update of the cache with market {market.lower()}")
                                continue
                            if int(stream_data['data']['U']) <= self.depth_caches[market.lower()]['last_update_id'] \
                                    <= int(stream_data['data']['u']):
                                # The first processed event should have U <= lastUpdateId AND u >= lastUpdateId
                                self._apply_updates(stream_data['data'], market=market.lower())
                                logger.info(f"BinanceLocalDepthCacheManager._process_stream_data() - Finished "
                                            f"initialization of the cache with market {market.lower()}")
                                # Init (refresh) finished
                                self.depth_caches[market.lower()]['is_synchronized'] = True
                                self.depth_caches[market.lower()]['last_refresh_time'] = int(time.time())
                    else:
                        # Regular depth update events
                        if self.exchange == "binance.com" or self.exchange == "binance.com-testnet":
                            if stream_data['data']['U'] != self.depth_caches[market.lower()]['last_update_id']+1:
                                logger.error(f"BinanceLocalDepthCacheManager._process_stream_data() - There is a "
                                             f"gap between the last and the penultimate update ID, the "
                                             f"depth_cache `{market.lower()}` is no longer correct and must be "
                                             f"reinitialized")
                                break
                        elif self.exchange == "binance.com-futures":
                            if stream_data['data']['pu'] != self.depth_caches[market.lower()]['last_update_id']:
                                logger.error(f"BinanceLocalDepthCacheManager._process_stream_data() - There is a "
                                             f"gap between the last and the penultimate update ID, the depth_cache "
                                             f"`{market.lower()}` is no longer correct and must be reinitialized")
                                break
                        if self.depth_caches[market.lower()]['refresh_interval'] is not None:
                            if self.depth_caches[market.lower()]['last_refresh_time'] < int(time.time()) - \
                                    self.depth_caches[market.lower()]['refresh_interval']:
                                logger.info(f"BinanceLocalDepthCacheManager._process_stream_data() - The refresh "
                                            f"interval has been exceeded, start new initialization for depth_cache "
                                            f"`{market.lower()}`")
                                break
                        logger.debug(f"BinanceLocalDepthCacheManager._process_stream_data() - Applying regular "
                                     f"depth update to the depth_cache with market {market.lower()} - update_id: "
                                     f"{stream_data['data']['U']} - {stream_data['data']['u']}")
                        self._apply_updates(stream_data['data'], market=market.lower())
                    self.depth_caches[market.lower()]['last_update_id'] = stream_data['data']['u']
                    self.depth_caches[market.lower()]['last_update_time'] = int(time.time())
                time.sleep(0.01)
        # Exiting ...
        del self.depth_caches[market.lower()]
        logger.info(f"BinanceLocalDepthCacheManager._process_stream_data() - depth_cache `{market.lower()}` was "
                    f"stopped and cleared")

    def _process_stream_signals(self):
        """
        Process stream_signals
        """
        logger.debug(f"BinanceLocalDepthCacheManager._process_stream_signals() - Started thread for stream_signals")
        while self.is_stop_request() is False:
            stream_signal = self.ubwa.pop_stream_signal_from_stream_signal_buffer()
            if stream_signal:
                logger.debug(f"BinanceLocalDepthCacheManager._process_stream_signals() - received stream_signal: "
                             f"{stream_signal}")
                for market in self.depth_caches:
                    if self.depth_caches[market]['stream_id'] == stream_signal['stream_id']:
                        if stream_signal['type'] == "DISCONNECT":
                            logger.debug(f"BinanceLocalDepthCacheManager._process_stream_signals() - Setting "
                                         f"stream_status of depth_cache with market {market} to `DISCONNECT")
                            self.depth_caches[market]['is_synchronized'] = False
                            self.depth_caches[market]['stream_status'] = "DISCONNECT"
                            self.ubwa.clear_stream_buffer(self.depth_caches[market.lower()]['stream_id'])
                            self.depth_caches[market]['refresh_request'] = True
                        elif stream_signal['type'] == "FIRST_RECEIVED_DATA":
                            logger.debug(f"BinanceLocalDepthCacheManager._process_stream_signals() - Setting "
                                         f"stream_status of depth_cache with market {market} to `RUNNING")
                            self.depth_caches[market]['stream_status'] = "RUNNING"
                        else:
                            logger.debug(f"BinanceLocalDepthCacheManager._process_stream_signals() - Setting "
                                         f"stream_status of depth_cache with market {market} to "
                                         f"`{stream_signal['type']}")
                            self.depth_caches[market]['stream_status'] = stream_signal['type']
            else:
                time.sleep(0.1)

    def _reset_depth_cache(self, market: str = None):
        """
        Reset a depth_cache (delete all asks and bids)

        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :return:
        """
        logger.debug(f"BinanceLocalDepthCacheManager._reset_depth_cache() - deleting all bids and ask of depth_cache "
                     f"with market {market.lower()}")
        with self.threading_lock_ask[market.lower()]:
            self.depth_caches[market.lower()]['asks'] = {}
        with self.threading_lock_bid[market.lower()]:
            self.depth_caches[market.lower()]['bids'] = {}

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
        logger.debug(f"BinanceLocalDepthCacheManager._sort_depth_cache() - Start sorting")
        new_items = [[float(price), float(quantity)] for price, quantity in items.items()]
        new_items = sorted(new_items, key=itemgetter(0), reverse=reverse)
        return new_items

    def create_depth_cache(self,
                           markets: Optional[Union[str, list]] = None,
                           update_interval: Optional[int] = None,
                           refresh_interval: int = None) -> bool:
        """
        Create one or more depth_cache!

        :param markets: Specify the market symbols for caches to be created
        :type markets: str or list
        :param update_interval: Update speed of the depth webstream in milliseconds. More info:
                                https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/wiki/update_intervals
        :type update_interval: int
        :param refresh_interval: The refresh interval in seconds, default is the `default_refresh_interval` of
                                 `BinanceLocalDepthCache <https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=default_refresh_interval#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager>`_.
        :type refresh_interval: int
        :return: bool
        """
        if markets is None:
            return False
        if isinstance(markets, str):
            markets = [markets, ]
        for market in markets:
            try:
                if self.depth_caches[market.lower()]:
                    logger.debug(f"BinanceLocalDepthCacheManager.create_depth_cache() - depth_cache "
                                 f"{market.lower()} already exists!")
                    return True
            except KeyError:
                logger.debug(f"BinanceLocalDepthCacheManager.create_depth_cache() - No existing depth_cache for "
                             f"market {market.lower()} found!")
            update_interval = update_interval or self.default_update_interval
            if update_interval is None:
                channel = f"depth"
            else:
                channel = f"depth@{update_interval}ms"
            stream_id = self.ubwa.create_stream(channel, market,
                                                stream_buffer_name=True,
                                                stream_label=f"ubldc_{market.lower()}",
                                                output="dict",
                                                ping_timeout=10,
                                                ping_interval=10,
                                                close_timeout=5)
            self._add_depth_cache(market=market.lower(), stream_id=stream_id, refresh_interval=refresh_interval)
            self.depth_caches[market.lower()]['thread'] = threading.Thread(target=self._process_stream_data,
                                                                           args=(market,))
            self.depth_caches[market.lower()]['thread'].start()
            while self.depth_caches[market.lower()]['thread_is_started'] is False:
                # This is to await the creation of the thread to avoid errors if the main thread gets closed before.
                # This can happen if after calling `create_depth_cache()` the main thread has no more code and exits.
                logger.debug(f"BinanceLocalDepthCacheManager.create_depth_cache() - Waiting till thread for "
                             f"market {market.lower()} is started")
                time.sleep(0.01)
        return True

    def get_asks(self, market: str = None) -> list:
        """
        Get the current asks

        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :return: list of asks with price and quantity.
        """
        if self.depth_caches[market.lower()]['is_synchronized'] is False:
            try:
                raise DepthCacheOutOfSync(f"The depth_cache for market symbol '{market.lower()}' is out of sync, "
                                          f"please try again later")
            except KeyError:
                raise KeyError(f"Invalid value provided: market={market.lower()}")

        if market:
            with self.threading_lock_ask[market.lower()]:
                return self._sort_depth_cache(self.depth_caches[market.lower()]['asks'], reverse=False)
        else:
            raise KeyError(f"Missing parameter `market`")

    def get_bids(self, market: str = None) -> list:
        """
        Get the current bids

        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :return: list of asks with price and quantity.
        """
        try:
            if self.depth_caches[market.lower()]['is_synchronized'] is False:
                raise DepthCacheOutOfSync(f"The depth_cache for market symbol '{market.lower()}' is out of sync, "
                                          f"please try again later")
        except KeyError:
            raise KeyError(f"Invalid value provided: market={market.lower()}")
        if market:
            with self.threading_lock_bid[market.lower()]:
                return self._sort_depth_cache(self.depth_caches[market.lower()]['bids'], reverse=True)
        else:
            raise KeyError(f"Missing parameter `market`")

    @staticmethod
    def get_latest_release_info() -> Optional[Union[dict, bool]]:
        """
        Get info about the latest available release

        :return: dict or False
        """
        logger.debug(f"BinanceLocalDepthCacheManager.get_latest_release_info() - Starting the request")
        try:
            respond = requests.get(f"https://api.github.com/repos/LUCIT-Systems-and-Development/"
                                   f"unicorn-binance-local-depth-cache/releases/latest")
            latest_release_info = respond.json()
            return latest_release_info
        except Exception:
            return False

    def get_latest_version(self) -> Optional[Union[str, bool]]:
        """
        Get the version of the latest available release (cache time 1 hour)

        :return: str or False
        """
        logger.debug(f"BinanceLocalDepthCacheManager.get_latest_version() - Starting the request")
        # Do a fresh request if status is None or last timestamp is older 1 hour
        if self.last_update_check_github['status'] is None or \
                (self.last_update_check_github['timestamp'] + (60 * 60) < time.time()):
            self.last_update_check_github['status'] = self.get_latest_release_info()
        if self.last_update_check_github['status']:
            try:
                return self.last_update_check_github['status']['tag_name']
            except KeyError:
                return "unknown"
        else:
            return "unknown"

    def get_list_of_depth_caches(self) -> list:
        """
        Get a list of existing depth caches

        :return: list
        """
        depth_cache_list = []
        for depth_cache in self.depth_caches:
            depth_cache_list.append(depth_cache)
        return depth_cache_list

    def is_depth_cache_synchronized(self, market: str = None) -> bool:
        """
        Is a specific depth_cache synchronized?

        :param market: Specify the market symbol for the used depth_cache
        :type market: str

        :return: bool
        """
        return self.depth_caches[market.lower()]['is_synchronized']

    def is_stop_request(self, market: str = None) -> bool:
        """
        Is there a stop request?

        :param market: Specify the market symbol for the used depth_cache
        :type market: str

        :return: bool
        """
        if market is None:
            if self.stop_request is False:
                return False
            else:
                return True
        else:
            if self.stop_request is False and self.depth_caches[market.lower()]['stop_request'] is False:
                return False
            else:
                return True

    def is_update_available(self) -> bool:
        """
        Is a new release of this package available?

        :return: bool
        """
        logger.debug(f"BinanceLocalDepthCacheManager.is_update_available() - Starting the request")
        installed_version = self.get_version()
        if ".dev" in installed_version:
            installed_version = installed_version[:-4]
        if self.get_latest_version() == installed_version:
            return False
        elif self.get_latest_version() == "unknown":
            return False
        else:
            return True

    def get_version(self):
        """
        Get the package/module version

        :return: str
        """
        return self.version

    def set_refresh_request(self, markets: Optional[Union[str, list]] = None) -> bool:
        """
        Set refresh requests for one or more depth_caches!

        :param markets: Specify the market symbols for the depth_caches to be refreshed
        :type markets: str or list
        :return: bool
        """
        if markets is None:
            logger.critical(f"BinanceLocalDepthCacheManager.set_refresh_request() - Please provide a market")
            return False
        if isinstance(markets, str):
            markets = [markets, ]
        for market in markets:
            logger.debug(f"BinanceLocalDepthCacheManager.set_refresh_request() - Set refresh request for "
                         f"depth_cache {market.lower()}")
            self.depth_caches[market.lower()]['refresh_request'] = True
        return True

    def stop_depth_cache(self, markets: Optional[Union[str, list]] = None) -> bool:
        """
        Stop and delete one or more depth_caches!

        :param markets: Specify the market symbols for the depth_caches to be stopped and deleted
        :type markets: str or list
        :return: bool
        """
        if markets is None:
            logger.critical(f"BinanceLocalDepthCacheManager.stop_depth_cache() - Please provide a market")
            return False
        if isinstance(markets, str):
            markets = [markets, ]
        for market in markets:
            logger.debug(f"BinanceLocalDepthCacheManager.stop_depth_cache() - Setting stop_request for "
                         f"depth_cache {market.lower()}, stop its stream and clear the stream_buffer")
            self.depth_caches[market.lower()]['stop_request'] = True
            self.ubwa.stop_stream(stream_id=self.depth_caches[market.lower()]['stream_id'])
            self.ubwa.clear_stream_buffer(stream_buffer_name=self.depth_caches[market.lower()]['stream_id'])
        return True

    def stop_manager_with_all_depth_caches(self) -> bool:
        """
        Stop unicorn-binance-local-depth-cache with all sub routines

        :return: bool
        """
        logger.debug(f"BinanceLocalDepthCacheManager.stop_manager_with_all_depth_caches - Stop initiated!")
        self.stop_request = True
        self.ubwa.stop_manager_with_all_streams()
        return True
