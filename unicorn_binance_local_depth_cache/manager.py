#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_local_depth_cache/manager.py
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
# Copyright (c) 2022-2024, LUCIT Systems and Development - https://www.lucit.tech
# All rights reserved.

from .exceptions import DepthCacheOutOfSync
from .licensing_manager import LucitLicensingManager, NoValidatedLucitLicense
from unicorn_binance_rest_api import BinanceRestApiManager, BinanceAPIException
from unicorn_binance_websocket_api import BinanceWebSocketApiManager
from operator import itemgetter
from typing import Optional, Callable

import cython
import logging
import platform
import requests
import time
import threading


__app_name__: str = "unicorn-binance-local-depth-cache"
__version__: str = "1.0.0.dev"
__logger__: logging = logging.getLogger("unicorn_binance_local_depth_cache")

logger = __logger__


class BinanceLocalDepthCacheManager(threading.Thread):
    """
    A Python SDK from LUCIT  to access and manage multiple local Binance DepthCaches with Python in a simple, fast,
    flexible, robust and fully-featured way.

    Binance API documentation:
    https://binance-docs.github.io/apidocs/spot/en/#how-to-manage-a-local-order-book-correctly
    https://binance-docs.github.io/apidocs/futures/en/#diff-book-depth-streams

    :param exchange: Select binance.com, binance.com-testnet, binance.com-futures, binance.com-futures-testnet
                     (default: binance.com)
    :type exchange: str
    :param default_refresh_interval: The default refresh interval in seconds, default is None.
    :type default_refresh_interval: int
    :param depth_update_interval: Update speed of the depth stream in milliseconds. More info:
                                  https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/wiki/update_intervals
    :type depth_update_interval: int
    :param process_depth_cache_signals: Provide a function/method to process the received stream signals. The function
                                        is running inside an asyncio loop and will be called instead of
                                        `add_to_stream_signal_buffer() <unicorn_binance_websocket_api.html#
                                        unicorn_binance_websocket_api.manager.BinanceWebSocketApiManager.add_to_stream_signal_buffer>`__
                                        like `process_stream_data(signal_type=False, stream_id=False,
                                        data_record=False)`.
    :type process_depth_cache_signals: function
    :param websocket_close_timeout: The `close_timeout` parameter defines a maximum wait time in seconds for
                                    completing the closing handshake and terminating the TCP connection.
                                    This parameter is passed through to the `websockets.client.connect()
                                    <https://websockets.readthedocs.io/en/stable/topics/design.html?highlight=close_timeout#closing-handshake>`__
    :type websocket_close_timeout: int
    :param websocket_ping_interval: Once the connection is open, a `Ping frame` is sent every
                                    `ping_interval` seconds. This serves as a keepalive. It helps keeping
                                    the connection open, especially in the presence of proxies with short
                                    timeouts on inactive connections. Set `ping_interval` to `None` to
                                    disable this behavior.
                                    This parameter is passed through to the `websockets.client.connect()
                                    <https://websockets.readthedocs.io/en/stable/topics/timeouts.html?highlight=ping_interval#keepalive-in-websockets>`__
    :type websocket_ping_interval: int
    :param websocket_ping_timeout: If the corresponding `Pong frame` isn't received within
                                   `ping_timeout` seconds, the connection is considered unusable and is closed with
                                   code 1011. This ensures that the remote endpoint remains responsive. Set
                                   `ping_timeout` to `None` to disable this behavior.
                                   This parameter is passed through to the `websockets.client.connect()
                                   <https://websockets.readthedocs.io/en/stable/topics/timeouts.html?highlight=ping_interval#keepalive-in-websockets>`_
    :type websocket_ping_timeout: int
    :param disable_colorama: set to True to disable the use of `colorama <https://pypi.org/project/colorama/>`_
    :type disable_colorama: bool
    :param ubra_manager: Provide a shared unicorn_binance_rest_api.manager instance
    :type ubra_manager: BinanceRestApiManager
    :param warn_on_update: set to `False` to disable the update warning
    :type warn_on_update: bool
    :param lucit_api_secret: The `api_secret` of your UNICORN Binance Suite license from
                             https://shop.lucit.services/software/unicorn-binance-suite
    :type lucit_api_secret:  str
    :param lucit_license_ini: Specify the path including filename to the config file (ex: `~/license_a.ini`). If not
                              provided lucitlicmgr tries to load a `lucit_license.ini` from `/home/oliver/.lucit/`.
    :type lucit_license_ini:  str
    :param lucit_license_profile: The license profile to use. Default is 'LUCIT'.
    :type lucit_license_profile:  str
    :param lucit_license_token: The `license_token` of your UNICORN Binance Suite license from
                                https://shop.lucit.services/software/unicorn-binance-suite
    :type lucit_license_token:  str
    """

    def __init__(self, exchange: str = "binance.com",
                 default_refresh_interval: int = None,
                 depth_update_interval: int = None,
                 process_depth_cache_signals: Optional[Callable, None] = None,
                 websocket_close_timeout: int = 2,
                 websocket_ping_interval: int = 10,
                 websocket_ping_timeout: int = 30,
                 disable_colorama: bool = False,
                 ubra_manager: BinanceRestApiManager = None,
                 warn_on_update: bool = True,
                 lucit_api_secret: str = None,
                 lucit_license_ini: str = None,
                 lucit_license_profile: str = None,
                 lucit_license_token: str = None):
        super().__init__()
        self.name = __app_name__
        self.version = __version__
        logger.info(f"New instance of {self.get_user_agent()}-{'compiled' if cython.compiled else 'source'} on "
                    f"{str(platform.system())} {str(platform.release())} for exchange {exchange} started ...")
        self.exchange = exchange
        self.depth_caches = {}
        self.depth_update_interval = depth_update_interval
        self.default_refresh_interval = default_refresh_interval
        self.websocket_close_timeout = websocket_close_timeout
        self.websocket_ping_interval = websocket_ping_interval
        self.websocket_ping_timeout = websocket_ping_timeout
        self.process_depth_cache_signals = process_depth_cache_signals
        self.disable_colorama = disable_colorama
        self.last_update_check_github = {'timestamp': time.time(), 'status': {'tag_name': None}}
        self.stop_request = False
        self.stream_id = None
        self.threading_lock_ask = {}
        self.threading_lock_bid = {}
        self.lucit_api_secret = lucit_api_secret
        self.lucit_license_ini = lucit_license_ini
        self.lucit_license_profile = lucit_license_profile
        self.lucit_license_token = lucit_license_token
        self.llm = LucitLicensingManager(api_secret=self.lucit_api_secret,
                                         license_ini=self.lucit_license_ini,
                                         license_profile=self.lucit_license_profile,
                                         license_token=self.lucit_license_token,
                                         parent_shutdown_function=self.stop_manager,
                                         program_used=self.name,
                                         needed_license_type="UNICORN-BINANCE-SUITE",
                                         start=True)
        licensing_exception = self.llm.get_license_exception()
        if licensing_exception is not None:
            raise NoValidatedLucitLicense(licensing_exception)
        if ubra_manager is None:
            try:
                self.ubra = BinanceRestApiManager(exchange=self.exchange,
                                                  disable_colorama=disable_colorama,
                                                  warn_on_update=warn_on_update,
                                                  lucit_api_secret=self.lucit_api_secret,
                                                  lucit_license_ini=self.lucit_license_ini,
                                                  lucit_license_profile=self.lucit_license_profile,
                                                  lucit_license_token=self.lucit_license_token)
            except requests.exceptions.ConnectionError as error_msg:
                error_msg = (f"Can not initialize BinanceLocalDepthCacheManager() - No internet connection? - "
                             f"{error_msg}")
                logger.critical(error_msg)
                raise ConnectionRefusedError(error_msg)
        else:
            self.ubra = ubra_manager
        self.ubwa = BinanceWebSocketApiManager(exchange=self.exchange,
                                               enable_stream_signal_buffer=True,
                                               disable_colorama=disable_colorama,
                                               process_stream_signals=self._process_stream_signals,
                                               close_timeout_default=self.websocket_close_timeout,
                                               ping_timeout_default=self.websocket_ping_interval,
                                               ping_interval_default=self.websocket_ping_timeout,
                                               warn_on_update=warn_on_update,
                                               lucit_api_secret=self.lucit_api_secret,
                                               lucit_license_ini=self.lucit_license_ini,
                                               lucit_license_profile=self.lucit_license_profile,
                                               lucit_license_token=self.lucit_license_token)
        if warn_on_update and self.is_update_available():
            update_msg = (f"Release {self.name}_{self.get_latest_version()} is available, please consider updating! "
                          f"Changelog: https://unicorn-binance-local-depth-cache.docs.lucit.tech/changelog.html")
            print(update_msg)
            logger.warning(update_msg)

    def __enter__(self):
        logger.debug(f"Entering 'with-context' ...")
        return self

    def __exit__(self, exc_type, exc_value, error_traceback):
        logger.debug(f"Leaving 'with-context' ...")
        self.stop_manager()
        if exc_type:
            logger.critical(f"An exception occurred: {exc_type} - {exc_value} - {error_traceback}")

    def _add_depth_cache(self,
                         market: str = None,
                         refresh_interval: int = None) -> bool:
        """
        Add a depth_cache to the depth_caches stack.

        :param market: Specify the market for the used depth_cache
        :type market: str
        :param refresh_interval: The refresh interval in seconds, default is the `default_refresh_interval` of
                                 `BinanceLocalDepthCache <https://unicorn-binance-local-depth-cache.docs.lucit.tech/
                                 unicorn_binance_local_depth_cache.html?highlight=default_refresh_interval#
                                 unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager>`__.
        :type refresh_interval: int
        :return: bool
        """
        logger.debug(f"BinanceLocalDepthCacheManager._add_depth_cache() - Adding new entry for market '{market}' ...")
        if market is not None:
            market = market.lower()
            self.depth_caches[market] = {'asks': {},
                                         'bids': {},
                                         'is_synchronized': False,
                                         'last_refresh_time': None,
                                         'last_update_id': None,
                                         'market': market,
                                         'refresh_interval': refresh_interval or self.default_refresh_interval,
                                         'refresh_request': True,
                                         'stop_request': False,
                                         'stream_status': None}
            self.threading_lock_ask[market] = threading.Lock()
            self.threading_lock_bid[market] = threading.Lock()
            logger.debug(f"BinanceLocalDepthCacheManager._add_depth_cache() - Added new entry for market '{market}'!")
            return True
        else:
            logger.critical(f"BinanceLocalDepthCacheManager._add_depth_cache() - Not able to add entry for market "
                            f"'{market}'!")
            return False

    def _add_ask(self, ask: list = None, market: str = None) -> bool:
        """
        Add, update or delete an ask of a specific depth_cache.

        :param ask: Add 'asks' to the depth_cache
        :type ask: list
        :param market: Specify the market for the used depth_cache
        :type market: str
        :return: bool
        """
        if ask is None or market is None:
            logger.debug(f"BinanceLocalDepthCacheManager._add_ask() - Parameter `ask` and `market` are mandatory!")
            return False
        market = market.lower()
        with self.threading_lock_ask[market]:
            self.depth_caches[market]['asks'][ask[0]] = float(ask[1])
            if ask[1] == "0.00000000" or ask[1] == "0.000":
                logger.debug(f"BinanceLocalDepthCacheManager._add_ask() - Deleting depth position {ask[0]} on ask "
                             f"side for market '{market}'")
                del self.depth_caches[market]['asks'][ask[0]]
            return True

    def _add_bid(self, bid: list = None, market: str = None) -> bool:
        """
        Add a bid to a specific depth_cache.

        :param bid: Add bids to the depth_cache
        :type bid: list
        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :return: bool
        """
        if bid is None or market is None:
            logger.debug(f"BinanceLocalDepthCacheManager._add_bid() - Parameter `bid` and `market` are mandatory!")
            return False
        market = market.lower()
        with self.threading_lock_bid[market]:
            self.depth_caches[market]['bids'][bid[0]] = float(bid[1])
            if bid[1] == "0.00000000" or bid[1] == "0.000":
                logger.debug(f"BinanceLocalDepthCacheManager._add_bid() - Deleting depth position {bid[0]} on bid "
                             f"side for market '{market}'")
                del self.depth_caches[market]['bids'][bid[0]]
            return True

    def _apply_updates(self, order_book: dict = None, market: str = None) -> bool:
        """
        Apply updates to a specific depth_cache

        :param order_book: Provide order_book data from rest or ws
        :type order_book: dict
        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :return: bool
        """
        if order_book is None or market is None:
            logger.debug(f"BinanceLocalDepthCacheManager._apply_updates() - Parameter `order_book` and `market` are "
                         f"mandatory!")
            return False
        market = market.lower()
        logger.debug(f"BinanceLocalDepthCacheManager._apply_updates() - Applying updates to the depth_cache with "
                     f"market {market}")
        for ask in order_book.get('a', []) + order_book.get('asks', []):
            self._add_ask(ask, market=market)
        for bid in order_book.get('b', []) + order_book.get('bids', []):
            self._add_bid(bid, market=market)
        return True

    def _get_order_book_from_rest(self, market: str = None) -> Optional[dict, None]:
        """
        Get the order_book snapshot via REST of the chosen market.

        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :return: dict or None
        """
        if market is not None:
            market = market.lower()
        current_weight = self.ubra.get_used_weight()
        while int(current_weight['weight']) > 4000:
            logger.warning(f"BinanceLocalDepthCacheManager._init_depth_cache() - The used weight "
                           f"({current_weight['weight']})of the Binance API is to high , waiting a few seconds ...")
            time.sleep(5)
        logger.info(f"Taking snapshot for market '{market}'! Current weight level is {current_weight}")
        try:
            if self.exchange == "binance.com" or self.exchange == "binance.com-testnet":
                try:
                    order_book = self.ubra.get_order_book(symbol=market.upper(), limit=1000)
                except BinanceAPIException as error_msg:
                    logger.error(f"BinanceLocalDepthCacheManager._init_depth_cache() - Can not download order_book "
                                 f"snapshot for the depth_cache with market {market} - BinanceAPIException - "
                                 f"error_msg: {error_msg}")
                    return None
            elif self.exchange == "binance.com-futures":
                try:
                    order_book = self.ubra.futures_order_book(symbol=market.upper(), limit=1000)
                except BinanceAPIException as error_msg:
                    logger.error(f"BinanceLocalDepthCacheManager._init_depth_cache() - Can not download order_book "
                                 f"snapshot for the depth_cache with market {market} - BinanceAPIException - "
                                 f"error_msg: {error_msg}")
                    return None
            else:
                return None
        except requests.exceptions.ConnectionError as error_msg:
            logger.error(f"BinanceLocalDepthCacheManager._init_depth_cache() - Can not download order_book snapshot "
                         f"for the depth_cache with market {market} - requests.exceptions.ConnectionError - "
                         f"error_msg: {error_msg}")

            return None
        except requests.exceptions.ReadTimeout as error_msg:
            logger.error(f"BinanceLocalDepthCacheManager._init_depth_cache() - Can not download order_book snapshot "
                         f"for the depth_cache with market {market} - requests.exceptions.ReadTimeout - "
                         f"error_msg: {error_msg}")
            return None
        logger.debug(f"BinanceLocalDepthCacheManager._init_depth_cache() - Downloaded order_book snapshot for "
                     f"the depth_cache with market {market}")
        return order_book

    def _init_depth_cache(self, market: str = None) -> bool:
        """
        Initialise the depth_cache with a rest snapshot.

        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :return: bool
        """
        logger.info(f"BinanceLocalDepthCacheManager._init_depth_cache() - Starting initialization of the cache "
                    f"with market {market}")
        if self.is_stop_request(market=market) is True:
            return False
        if market is not None:
            market = market.lower()
        order_book = self._get_order_book_from_rest(market=market)
        if order_book is None:
            logger.info(f"BinanceLocalDepthCacheManager._init_depth_cache() - Can not get order_book of the cache "
                        f"with market {market}")
            return False
        self._reset_depth_cache(market=market)
        self.depth_caches[market]['last_refresh_time'] = int(time.time())
        self.depth_caches[market]['last_update_time'] = int(time.time())
        try:
            self.depth_caches[market]['last_update_id'] = int(order_book['lastUpdateId'])
        except TypeError as error_msg:
            logger.error(f"BinanceLocalDepthCacheManager._init_depth_cache() - TypeError - error_msg: {error_msg}")
            return False
        self._apply_updates(order_book, market=market)
        for bid in order_book['bids']:
            self._add_bid(bid, market=market)
        for ask in order_book['asks']:
            self._add_ask(ask, market=market)
        logger.debug(f"BinanceLocalDepthCacheManager._init_depth_cache() - Finished initialization of the cache "
                     f"with market {market}")
        return True

    async def _manage_depth_cache_async(self, stream_id=None) -> None:
        """
        Process depth stream_data and manage the depth cache

        The logic is described here:
        - `Binance Spot <https://developers.binance.com/docs/binance-api/spot-detail/web-socket-streams#
        how-to-manage-a-local-order-book-correctly>`__
        - `Binance Futures <https://binance-docs.github.io/apidocs/futures/en/#diff-book-depth-streams>`__

        :param stream_id:
        :type stream_id: str
        :return: None
        """
        logger.debug(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - Start processing data from "
                     f"webstream {self.ubwa.get_stream_label(stream_id=stream_id)}")
        while self.ubwa.is_stop_request(stream_id=stream_id) is False:
            stream_data = await self.ubwa.get_stream_data_from_asyncio_queue(stream_id=stream_id)
            if "'error':" in str(stream_data):
                logger.error(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - Received error message: "
                             f"{stream_data}")
                self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                continue
            elif "'result':" in str(stream_data):
                logger.debug(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - Received result message: "
                             f"{stream_data}")
                self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                continue
            market = str(stream_data['stream'].split('@')[0]).lower()
            logger.debug(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - Extracted market from stream "
                         f"data: {market}")
            if self.is_stop_request(market=market) is True:
                return None
            if self.depth_caches.get(market) is None:
                logger.error(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - `depth_cache` for {market}"
                             f"does not exists!")
                self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                continue
            if self.depth_caches[market]['refresh_request'] is True:
                logger.info(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - Caught refresh_request "
                            f"for depth_cache with market {market}")

                thread = threading.Thread(target=self._init_depth_cache, args=(market,))
                thread.start()

                self.depth_caches[market]['refresh_request'] = False
                self.depth_caches[market]['is_synchronized'] = False
            if self.depth_caches[market]['last_update_id'] is None:
                continue
            if self.depth_caches[market]['is_synchronized'] is False:
                logger.info(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - Init depth cache of market "
                            f"{market}")
                if self.exchange == "binance.com" or self.exchange == "binance.com-testnet":
                    if int(stream_data['data']['u']) <= self.depth_caches[market]['last_update_id']:
                        # Drop it
                        logger.debug(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - Dropping "
                                     f"outdated depth update of the cache with market {market}")
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                    if int(stream_data['data']['U']) <= self.depth_caches[market]['last_update_id']+1 \
                            <= int(stream_data['data']['u']):
                        # The first processed event should have U <= lastUpdateId+1 AND u >= lastUpdateId+1.
                        self._apply_updates(stream_data['data'], market=market)
                        logger.info(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - Finished "
                                    f"initialization of the cache with market {market}")
                        # Init (refresh) finished
                        last_sync_time = time.time()
                        self.depth_caches[market]['last_update_id'] = int(stream_data['data']['u'])
                        self.depth_caches[market]['last_update_time'] = int(last_sync_time)
                        self.depth_caches[market]['last_refresh_time'] = int(last_sync_time)
                        self.depth_caches[market]['is_synchronized'] = True
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                elif self.exchange == "binance.com-futures":
                    if int(stream_data['data']['u']) < self.depth_caches[market]['last_update_id']:
                        # Drop it
                        logger.debug(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - Dropping "
                                     f"outdated depth update of the cache with market {market}")
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                    if int(stream_data['data']['U']) <= self.depth_caches[market]['last_update_id'] \
                            <= int(stream_data['data']['u']):
                        # The first processed event should have U <= lastUpdateId AND u >= lastUpdateId
                        self._apply_updates(stream_data['data'], market=market)
                        logger.info(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - Finished "
                                    f"initialization of the cache with market {market}")
                        # Init (refresh) finished
                        last_sync_time = time.time()
                        self.depth_caches[market]['last_update_id'] = int(stream_data['data']['u'])
                        self.depth_caches[market]['last_update_time'] = int(last_sync_time)
                        self.depth_caches[market]['last_refresh_time'] = int(last_sync_time)
                        self.depth_caches[market]['is_synchronized'] = True
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
            else:
                # Gap detection
                if self.exchange == "binance.com" or self.exchange == "binance.com-testnet":
                    if stream_data['data']['U'] != self.depth_caches[market]['last_update_id']+1:
                        logger.error(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - There is a "
                                     f"gap between the last and the penultimate update ID, the "
                                     f"depth_cache `{market}` is no longer correct and must be "
                                     f"reinitialized")
                        self.depth_caches[market]['is_synchronized'] = False
                        self.depth_caches[market]['refresh_request'] = True
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                elif self.exchange == "binance.com-futures":
                    if stream_data['data']['pu'] != self.depth_caches[market]['last_update_id']:
                        logger.error(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - There is a "
                                     f"gap between the last and the penultimate update ID, the depth_cache "
                                     f"`{market}` is no longer correct and must be reinitialized")
                        self.depth_caches[market]['is_synchronized'] = False
                        self.depth_caches[market]['refresh_request'] = True
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                if self.depth_caches[market]['refresh_interval'] is not None:
                    if self.depth_caches[market]['last_refresh_time'] < int(time.time()) - \
                            self.depth_caches[market]['refresh_interval']:
                        logger.info(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - The refresh "
                                    f"interval has been exceeded, start new initialization for depth_cache "
                                    f"`{market}`")
                        self.depth_caches[market]['is_synchronized'] = False
                        self.depth_caches[market]['refresh_request'] = True
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                # Regular updates -> apply
                logger.debug(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - Applying regular "
                             f"depth update to the depth_cache with market {market} - update_id: "
                             f"{stream_data['data']['U']} - {stream_data['data']['u']}")
                self._apply_updates(stream_data['data'], market=market)
                self.depth_caches[market]['last_update_id'] = int(stream_data['data']['u'])
                self.depth_caches[market]['last_update_time'] = int(time.time())
                self.ubwa.asyncio_queue_task_done(stream_id=stream_id)

    def _process_stream_signals(self, signal_type=None, stream_id=None, data_record=None, error_msg=None) -> None:
        """
        Process stream_signals

        :return: None
        """
        logger.debug(f"BinanceLocalDepthCacheManager._process_stream_signals() - received stream_signal: "
                     f"{signal_type} - {stream_id} - {data_record} - {error_msg}")
        if self.is_stop_request() is True:
            return None

        for market in self.depth_caches:
            if signal_type == "DISCONNECT":
                logger.debug(f"BinanceLocalDepthCacheManager._process_stream_signals() - Setting "
                             f"stream_status of depth_cache with market {market} to `DISCONNECTED")
                self.depth_caches[market]['is_synchronized'] = False
                self.depth_caches[market]['refresh_request'] = True
                self.depth_caches[market]['stream_status'] = "DISCONNECTED"
            elif signal_type == "FIRST_RECEIVED_DATA":
                logger.debug(f"BinanceLocalDepthCacheManager._process_stream_signals() - Setting "
                             f"stream_status of depth_cache with market {market} to `RUNNING")
                self.depth_caches[market]['stream_status'] = "RUNNING"
            else:
                logger.debug(f"BinanceLocalDepthCacheManager._process_stream_signals() - Setting "
                             f"stream_status of depth_cache with market {market} to "
                             f"`{signal_type}")
                self.depth_caches[market]['stream_status'] = signal_type

    def _reset_depth_cache(self, market: str = None) -> bool:
        """
        Reset a depth_cache (delete all asks and bids)

        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :return: bool
        """
        if market is not None:
            market = market.lower()
        logger.debug(f"BinanceLocalDepthCacheManager._reset_depth_cache() - deleting all bids and ask of depth_cache "
                     f"with market {market}")
        with self.threading_lock_ask[market]:
            self.depth_caches[market]['asks'] = {}
        with self.threading_lock_bid[market]:
            self.depth_caches[market]['bids'] = {}
        return True

    @staticmethod
    def _sort_depth_cache(items, reverse=False) -> list:
        """
        Sort asks or bids by price

        :param items: asks or bids
        :type items: dict
        :param reverse: False is regular, True is reversed
        :type reverse: bool
        :return: list
        """
        logger.debug(f"BinanceLocalDepthCacheManager._sort_depth_cache() - Start sorting")
        new_items = [[float(price), float(quantity)] for price, quantity in items.items()]
        new_items = sorted(new_items, key=itemgetter(0), reverse=reverse)
        return new_items

    def _subscribe_depth(self, markets: Optional[str, list] = None) -> bool:
        if markets is None:
            return False
        if isinstance(markets, str):
            markets = [markets, ]
        if self.depth_update_interval is None:
            channel = f"depth"
        else:
            channel = f"depth@{self.depth_update_interval}ms"

        if self.get_stream_id() is None:
            self.stream_id = self.ubwa.create_stream(channels=channel,
                                                     markets=markets,
                                                     stream_label=f"ubldc_depth",
                                                     output="dict",
                                                     process_asyncio_queue=self._manage_depth_cache_async)
        else:
            self.ubwa.subscribe_to_stream(stream_id=self.stream_id, markets=markets)

    def create_depth_cache(self,
                           markets: Optional[str, list] = None,
                           refresh_interval: int = None) -> bool:
        """
        Create one or more depth_cache!

        :param markets: Specify the market symbols for caches to be created
        :type markets: str or list
        :param refresh_interval: The refresh interval in seconds, default is the `default_refresh_interval` of
                                 `BinanceLocalDepthCache <https://unicorn-binance-local-depth-cache.docs.lucit.tech/
                                 unicorn_binance_local_depth_cache.html?highlight=default_refresh_interval#
                                 unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager>`__.
        :type refresh_interval: int

        :return: bool
        """
        if markets is None:
            return False

        if type(markets) is list:
            for market in markets:
                self._add_depth_cache(market=market, refresh_interval=refresh_interval)
        else:
            self._add_depth_cache(market=markets, refresh_interval=refresh_interval)
        self._subscribe_depth(markets=markets)
        return True

    def get_asks(self, market: str = None, depth: Optional[int] = None) -> list:
        """
        Get the current list of asks with price and quantity.

        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :param depth: Define the level from which pruning takes place.
        :type depth: int or None (0 is nothing, None is everything)
        :return: list
        """
        if market is not None:
            market = market.lower()
        try:
            if self.depth_caches[market]['is_synchronized'] is False:
                try:
                    raise DepthCacheOutOfSync(f"The depth_cache for market symbol '{market}' is out of sync, "
                                              f"please try again later")
                except KeyError:
                    raise KeyError(f"Invalid value provided: market={market}")
        except KeyError:
            raise DepthCacheOutOfSync(f"The depth_cache for market symbol '{market}' is out of sync, "
                                      f"please try again later")
        if market:
            with self.threading_lock_ask[market]:
                return self._sort_depth_cache(self.depth_caches[market]['asks'], reverse=False)[:depth]
        else:
            raise KeyError(f"Missing parameter `market`")

    def get_bids(self, market: str = None, depth: Optional[int] = None) -> list:
        """
        Get the current list of bids with price and quantity.

        :param market: Specify the market symbol for the used depth_cache.
        :type market: str
        :param depth: Define the level from which pruning takes place.
        :type depth: int or None (0 is nothing, None is everything)
        :return: list
        """
        if market is not None:
            market = market.lower()
        try:
            if self.depth_caches[market]['is_synchronized'] is False:
                raise DepthCacheOutOfSync(f"The depth_cache for market symbol '{market}' is out of sync, "
                                          f"please try again later")
        except KeyError:
            raise KeyError(f"Invalid value provided: market={market}")
        if market:
            with self.threading_lock_bid[market]:
                return self._sort_depth_cache(self.depth_caches[market]['bids'], reverse=True)[:depth]
        else:
            raise KeyError(f"Missing parameter `market`")

    @staticmethod
    def get_latest_release_info() -> Optional[dict, None]:
        """
        Get info about the latest available release

        :return: dict or None
        """
        logger.debug(f"BinanceLocalDepthCacheManager.get_latest_release_info() - Starting the request")
        try:
            respond = requests.get(f"https://api.github.com/repos/LUCIT-Systems-and-Development/"
                                   f"unicorn-binance-local-depth-cache/releases/latest")
            latest_release_info = respond.json()
            return latest_release_info
        except Exception as error_msg:
            logger.error(f"BinanceLocalDepthCacheManager.get_latest_release_info() - Exception - "
                         f"error_msg: {error_msg}")
            return None

    def get_latest_version(self) -> Optional[str]:
        """
        Get the version of the latest available release (cache time 1 hour)

        :return: str
        """
        logger.debug(f"BinanceLocalDepthCacheManager.get_latest_version() - Starting the request")
        # Do a fresh request if status is None or last timestamp is older 1 hour

        if self.last_update_check_github['status'].get('tag_name') is None or \
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
        logger.debug(f"BinanceLocalDepthCacheManager.get_list_of_depth_caches() - Create and then return the list")
        depth_cache_list = []
        for depth_cache in self.depth_caches:
            depth_cache_list.append(depth_cache)
        return depth_cache_list

    def get_ubra_manager(self):
        """
        Get the used BinanceRestApiManager() instance of BinanceLocalDepthCacheManager()

        :return: BinanceRestApiManager
        """
        return self.ubra

    def get_ubwa_manager(self):
        """
        Get the used BinanceWebSocketApiManager() instance of BinanceLocalDepthCacheManager()

        :return: BinanceWebSocketApiManager
        """
        return self.ubwa

    def get_user_agent(self):
        """
        Get the user_agent string "lib name + lib version + python version"

        :return:
        """
        user_agent = f"{self.name}_{str(self.get_version())}-python_{str(platform.python_version())}"
        return user_agent

    def is_depth_cache_synchronized(self, market: str = None) -> bool:
        """
        Is a specific depth_cache synchronized?

        :param market: Specify the market symbol for the used depth_cache
        :type market: str

        :return: bool
        """
        if market is not None:
            market = market.lower()
        logger.debug(f"BinanceLocalDepthCacheManager.is_depth_cache_synchronized() - Returning the status")
        try:
            return self.depth_caches[market]['is_synchronized']
        except KeyError:
            return False

    def is_stop_request(self, market: str = None) -> bool:
        """
        Is there a stop request?

        :param market: Specify the market symbol for the used depth_cache
        :type market: str

        :return: bool
        """
        if market is not None:
            market = market.lower()
        logger.debug(f"BinanceLocalDepthCacheManager.is_stop_request() - Returning the status for market '{market}'")
        if market is None:
            if self.stop_request is False:
                return False
            else:
                return True
        else:
            try:
                if self.stop_request is False and self.depth_caches[market]['stop_request'] is False:
                    return False
                else:
                    return True
            except KeyError:
                return False

    def get_stream_id(self) -> str:
        """
        Get the stream_id of the stream.

        :return: stream_id (str)
        """
        return self.stream_id

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

    def get_version(self) -> str:
        """
        Get the package/module version

        :return: str
        """
        logger.debug(f"BinanceLocalDepthCacheManager.get_version() - Returning the version")
        return self.version

    def print_summary(self, add_string=None, title=None):
        """
        Print an overview of all streams

        :param add_string: text to add to the output
        :type add_string: str
        :param title: title of the output
        :type title: str
        """
        if title is None:
            title = self.get_user_agent()
        self.ubwa.print_summary(add_string=add_string, title=title)

    def set_refresh_request(self, markets: Optional[str, list] = None) -> bool:
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
            market = market.lower()
            logger.info(f"BinanceLocalDepthCacheManager.set_refresh_request() - Set refresh request for "
                        f"depth_cache {market}")
            self.depth_caches[market]['refresh_request'] = True
        return True

    def stop_depth_cache(self, markets: Optional[str, list] = None) -> bool:
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
            market = market.lower()
            logger.info(f"BinanceLocalDepthCacheManager.stop_depth_cache() - Setting stop_request for "
                        f"depth_cache {market}, stop its stream and clear the stream_buffer")
            self.depth_caches[market]['stop_request'] = True
            self.ubwa.unsubscribe_from_stream(stream_id=self.get_stream_id(), markets=market)
        return True

    def stop_manager(self, close_api_session: bool = True) -> bool:
        """
        Stop unicorn-binance-local-depth-cache with all sub routines

        :return: bool
        """
        logger.debug(f"BinanceLocalDepthCacheManager.stop_manager() - Stop initiated!")
        self.stop_request = True
        self.ubra.stop_manager()
        self.ubwa.stop_manager()
        if close_api_session is True:
            self.llm.close()
        return True
