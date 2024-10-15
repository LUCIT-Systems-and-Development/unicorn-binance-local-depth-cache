#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
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

from .cluster import Cluster
from .exceptions import *
from .licensing_manager import LucitLicensingManager, NoValidatedLucitLicense
from requests import ConnectionError
from unicorn_binance_rest_api import BinanceRestApiManager, BinanceAPIException, AlreadyStoppedError
from unicorn_binance_websocket_api import BinanceWebSocketApiManager
from operator import itemgetter
from typing import Optional, Union, Generator, Dict, List

import cython
import logging
import platform
import requests
import time
import threading


__app_name__: str = "unicorn-binance-local-depth-cache"
__version__: str = "2.3.0"
__logger__: logging.getLogger = logging.getLogger("unicorn_binance_local_depth_cache")

logger = __logger__


class BinanceLocalDepthCacheManager(threading.Thread):
    """
    A Python SDK by LUCIT  to access and manage multiple local Binance DepthCaches with Python in a simple, fast,
    flexible, robust and fully-featured way.

    Binance API documentation:
        - https://binance-docs.github.io/apidocs/spot/en/#how-to-manage-a-local-order-book-correctly
        - https://binance-docs.github.io/apidocs/futures/en/#diff-book-depth-streams

    :param exchange: Select binance.com, binance.com-testnet, binance.com-futures, binance.com-futures-testnet
                     (default: binance.com)
    :type exchange: str
    :param default_refresh_interval: The default refresh interval in seconds, default is None. The depth_cache is reset
                                     and reinitialized at this interval.
    :type default_refresh_interval: int
    :param init_time_window: Only one request to the Binance REST API is permitted per depth_cache in this time window
                             (specified in seconds).
    :type init_time_window: int (seconds)
    :param high_performance: If True, access to the depth snapshots via REST in the INIT process is not regulated.
                             Be careful!
    :type high_performance:  bool
    :param depth_cache_update_interval: Update speed of the depth stream in milliseconds. More info:
                                        https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/wiki/update_intervals
    :type depth_cache_update_interval: int
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
                 depth_cache_update_interval: int = None,
                 high_performance: bool = False,
                 init_interval: float = 0.5,
                 init_time_window: int = 5,
                 websocket_close_timeout: int = 2,
                 websocket_ping_interval: int = 10,
                 websocket_ping_timeout: int = 20,
                 disable_colorama: bool = False,
                 ubdcc_address: str = None,
                 ubdcc_port: int = 80,
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
        self.depth_caches: dict = {}
        self.depth_cache_update_interval = depth_cache_update_interval
        self.default_refresh_interval = default_refresh_interval
        self.high_performance = high_performance
        self.init_interval = init_interval
        self.init_time_window = init_time_window
        self.websocket_close_timeout = websocket_close_timeout
        self.websocket_ping_interval = websocket_ping_interval
        self.websocket_ping_timeout = websocket_ping_timeout
        self.disable_colorama = disable_colorama
        self.ubdcc_address = ubdcc_address
        self.ubdcc_port = ubdcc_port
        self.last_update_check_github: dict = {'timestamp': time.time(), 'status': {'tag_name': None}}
        self.stop_request: bool = False
        self.stream_status: Optional[str] = None
        self.threading_lock_ask: dict = {}
        self.threading_lock_bid: dict = {}
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

        if self.ubdcc_address is not None:
            self.cluster = Cluster(address=self.ubdcc_address, port=self.ubdcc_port)
        else:
            self.cluster = None

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

        self.websockets = {}

        if self.high_performance is True:
            logger.info(f"Using `high_performance` ...")
        self._gen_get_init_slot = self._generator_get_init_slot()
        next(self._gen_get_init_slot)

        if warn_on_update is True and self.is_update_available() is True:
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
        `BinanceLocalDepthCache <https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=default_refresh_interval#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager>`__.
        The depth_cache is reset and reinitialized at this interval.
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
            if float(ask[1]) == 0.0:
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
            if float(bid[1]) == 0.0:
                logger.debug(f"BinanceLocalDepthCacheManager._add_bid() - Deleting depth position {bid[0]} on bid "
                             f"side for market '{market}'")
                del self.depth_caches[market]['bids'][bid[0]]
            return True

    def _apply_updates(self, asks: list = None, bids: list = None, market: str = None) -> bool:
        """
        Apply updates to a specific depth_cache

        :param asks: Provide asks data
        :type asks: list
        :param bids: Provide bids data
        :type bids: list
        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :return: bool
        """
        if asks is None or bids is None or market is None:
            logger.debug(f"BinanceLocalDepthCacheManager._apply_updates() - Parameter `asks`, `bids` and `market` are "
                         f"mandatory!")
            return False
        market = market.lower()
        logger.debug(f"BinanceLocalDepthCacheManager._apply_updates() - Applying updates to the depth_cache with "
                     f"market {market}")
        for ask in asks:
            self._add_ask(ask, market=market)
        for bid in bids:
            self._add_bid(bid, market=market)
        return True

    def _get_order_book_from_rest(self, market: str = None) -> Optional[dict]:
        """
        Get the order_book snapshot via REST of the chosen market.

        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :return: dict or None
        """
        if market is not None:
            market = market.lower()
        logger.info(f"Taking snapshot for market '{market}'!")
        try:
            if self.exchange == "binance.com" \
                    or self.exchange == "binance.com-testnet" \
                    or self.exchange == "binance.us":
                order_book = self.ubra.get_order_book(symbol=market.upper(), limit=1000)
            elif self.exchange == "binance.com-futures" or self.exchange == "binance.com-futures-testnet":
                order_book = self.ubra.futures_order_book(symbol=market.upper(), limit=1000)
            else:
                return None
        except BinanceAPIException as error_msg:
            logger.error(f"BinanceLocalDepthCacheManager._get_order_book_from_rest() - Can not download "
                         f"order_book snapshot for the depth_cache with market {market} - BinanceAPIException "
                         f"- error_msg: {error_msg}")
            return None
        except AlreadyStoppedError as error_msg:
            logger.debug(f"BinanceLocalDepthCacheManager._get_order_book_from_rest() - AlreadyStoppedError - "
                         f"error_msg: {error_msg}")
            return None
        except requests.exceptions.ConnectionError as error_msg:
            logger.error(f"BinanceLocalDepthCacheManager._get_order_book_from_rest() - Can not download order_book "
                         f"snapshot for the depth_cache with market {market} - requests.exceptions.ConnectionError - "
                         f"error_msg: {error_msg}")

            return None
        except requests.exceptions.ReadTimeout as error_msg:
            logger.error(f"BinanceLocalDepthCacheManager._get_order_book_from_rest() - Can not download order_book "
                         f"snapshot for the depth_cache with market {market} - requests.exceptions.ReadTimeout - "
                         f"error_msg: {error_msg}")
            return None
        logger.debug(f"BinanceLocalDepthCacheManager._init_depth_get_order_book_from_rest_cache() - Downloaded "
                     f"order_book snapshot for the depth_cache with market {market}")
        return order_book

    def _generator_get_init_slot(self) -> Generator[str, str, None]:
        """
        Get a free init slot.

        The generator controls the INIT processes for DepthCaches. Only a total of 1 INIT signal is issued per
        `init_interval` for all markets, and only once per depth cache in `self.init_time_window`.

        :return: str "INIT" or "DROP"
        """
        last_yield_time: Dict[str, float] = {}
        last_global_yield_time: float = 0.0
        lock = threading.Lock()

        while True:
            id_received = yield
            with (lock):
                current_time = time.time()
                if id_received not in last_yield_time \
                        or current_time - last_yield_time[id_received] >= self.init_time_window:
                    last_yield_time[id_received] = current_time

                    if current_time - last_global_yield_time >= self.init_interval:
                        last_global_yield_time = current_time
                        yield "INIT"
                    else:
                        yield "DROP"
                else:
                    yield "DROP"

    def _init_depth_cache(self, market: str = None) -> bool:
        """
        Initialise the depth_cache with a rest snapshot.

        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :return: bool
        """
        logger.info(f"BinanceLocalDepthCacheManager._init_depth_cache(market={market}) - Starting initialization ...")
        if self.is_stop_request(market=market) is True:
            return False
        if market is not None:
            market = market.lower()
        try:
            order_book = self._get_order_book_from_rest(market=market)
        except ConnectionError as error_msg:
            logger.error(f"BinanceLocalDepthCacheManager._init_depth_cache(market={market}) - ConnectionError: "
                         f"{error_msg}")
            self.depth_caches[market]['refresh_request'] = True
            return False
        if order_book is None:
            logger.info(f"BinanceLocalDepthCacheManager._init_depth_cache(market={market}) - Can not get order_book!")
            self.depth_caches[market]['refresh_request'] = True
            return False
        self._reset_depth_cache(market=market)
        self.depth_caches[market]['last_refresh_time'] = int(time.time())
        self.depth_caches[market]['last_update_time'] = int(time.time())
        try:
            self.depth_caches[market]['last_update_id'] = int(order_book['lastUpdateId'])
        except TypeError as error_msg:
            logger.error(f"BinanceLocalDepthCacheManager._init_depth_cache(market={market}) - TypeError: {error_msg}")
            self.depth_caches[market]['refresh_request'] = True
            return False
        except KeyError as error_msg:
            logger.error(f"BinanceLocalDepthCacheManager._init_depth_cache(market={market}) - KeyError: {error_msg}")
            self.depth_caches[market]['refresh_request'] = True
            return False
        self._apply_updates(asks=order_book['asks'], bids=order_book['bids'], market=market)
        logger.debug(f"BinanceLocalDepthCacheManager._init_depth_cache(market={market}) - Finished initialization!")
        return True

    async def _manage_depth_cache_async(self, stream_id=None) -> None:
        """
        Process depth stream_data and manage the depth cache

        The logic is described here:
        - `Binance Spot <https://developers.binance.com/docs/binance-api/spot-detail/web-socket-streams#
        how-to-manage-a-local-order-book-correctly>`__
        - `Binance Futures <https://binance-docs.github.io/apidocs/futures/en/#diff-book-depth-streams>`__

        :param stream_id: ID of the UBWA stream
        :type stream_id: str
        :return: None
        """
        logger.debug(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) - Start "
                     f"processing data from stream `{self.ubwa.get_stream_label(stream_id=stream_id)}`")
        while self.ubwa.is_stop_request(stream_id=stream_id) is False:
            stream_data = await self.ubwa.get_stream_data_from_asyncio_queue(stream_id=stream_id)
            # Filter and proof requests
            if "'result':" in str(stream_data) or "'error':" in str(stream_data):
                logger.error(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) - "
                             f"Received system message: {stream_data}")
                self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                continue
            market = str(stream_data['stream'].split('@')[0]).lower()
            logger.debug(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) - Extracted "
                         f"market from stream data: {market}")
            if self.is_stop_request(market=market) is True:
                logger.debug(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) - "
                             f"depth_cache for market {market} is stopping!")
                self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                continue
            if self.depth_caches.get(market) is None:
                logger.error(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) - "
                             f"`depth_cache` for {market} does not exists!")
                self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                continue
            if self.depth_caches[market]['refresh_request'] is True:
                logger.debug(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) - Caught "
                             f"refresh_request for depth_cache with market {market} ...")
                self.depth_caches[market]['is_synchronized'] = False
                if self._gen_get_init_slot.send(market) == "INIT" or self.high_performance is True:
                    logger.debug(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) - "
                                 f"Depth init for {market} started at {time.time()}!")
                    try:
                        current_weight = self.ubra.get_used_weight()
                    except BinanceAPIException as error_msg:
                        logger.error(f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - Can not get used "
                                     f"weight for market {market} - BinanceAPIException - error_msg: {error_msg}")
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                    except AlreadyStoppedError as error_msg:
                        logger.debug(
                            f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - Can not get used "
                            f"weight for market {market} - AlreadyStoppedError - error_msg: {error_msg}")
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                    except requests.exceptions.ConnectionError as error_msg:
                        logger.error(
                            f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - Can not get used "
                            f"weight for market {market} - requests.exceptions.ConnectionError - "
                            f"error_msg: {error_msg}")
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                    except requests.exceptions.ReadTimeout as error_msg:
                        logger.error(
                            f"BinanceLocalDepthCacheManager._manage_depth_cache_async() - Can not get used "
                            f"weight for market {market} - requests.exceptions.ReadTimeout - error_msg: {error_msg}")
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                    if current_weight['weight'] > 2200 or current_weight['status_code'] != 200:
                        logger.warning(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id})"
                                       f" - The used weight ({current_weight['weight']}) of the Binance API is to high "
                                       f"or the status_code {current_weight['status_code']} != 200, market {market} is "
                                       f"waiting a few seconds ...")
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                    logger.info(f"Taking snapshot for market '{market}'! Current weight level is {current_weight}!")
                    self.depth_caches[market]['refresh_request'] = False
                    self.depth_caches[market]['last_update_id'] = None
                    thread = threading.Thread(target=self._init_depth_cache, args=(market,))
                    thread.start()

            # Processing depth data
            if self.depth_caches[market]['is_synchronized'] is True:
                # Regular updates
                # Gap detection
                if self.exchange == "binance.com" \
                        or self.exchange == "binance.com-testnet" \
                        or self.exchange == "binance.us":
                    if stream_data['data']['U'] != self.depth_caches[market]['last_update_id']+1:
                        logger.error(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) "
                                     f"- There is a gap between the last and the penultimate update ID, the depth_cache"
                                     f" `{market}` is no longer correct and must be reinitialized")
                        self.depth_caches[market]['is_synchronized'] = False
                        self.depth_caches[market]['refresh_request'] = True
                        self.depth_caches[market]['last_update_id'] = None
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                elif self.exchange == "binance.com-futures" or self.exchange == "binance.com-futures-testnet":
                    if stream_data['data']['pu'] != self.depth_caches[market]['last_update_id']:
                        logger.error(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) "
                                     f"- There is a gap between the last and the penultimate update ID, the depth_cache"
                                     f" `{market}` is no longer correct and must be reinitialized")
                        self.depth_caches[market]['is_synchronized'] = False
                        self.depth_caches[market]['refresh_request'] = True
                        self.depth_caches[market]['last_update_id'] = None
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                if self.depth_caches[market]['refresh_interval'] is not None:
                    if self.depth_caches[market]['last_refresh_time'] < int(time.time()) - \
                            self.depth_caches[market]['refresh_interval']:
                        logger.info(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) "
                                    f"- The refresh interval has been exceeded, start new initialization for "
                                    f"depth_cache `{market}`")
                        self.depth_caches[market]['is_synchronized'] = False
                        self.depth_caches[market]['refresh_request'] = True
                        self.depth_caches[market]['last_update_id'] = None
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                # Apply updates
                logger.debug(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) - "
                             f"Applying regular depth update to the depth_cache with market {market} - update_id: "
                             f"{stream_data['data']['U']} - {stream_data['data']['u']}")
                self._apply_updates(asks=stream_data['data']['a'], bids=stream_data['data']['b'], market=market)
                self.depth_caches[market]['last_update_id'] = int(stream_data['data']['u'])
                self.depth_caches[market]['last_update_time'] = int(time.time())
                self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                continue
            else:
                logger.info(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) - Init "
                            f"depth cache of market {market}")
                if self.depth_caches[market]['last_update_id'] is None:
                    logger.debug(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) - "
                                 f"Dropping outdated depth update of the cache with market {market}! Reason: "
                                 f"`last_update_id` is None")
                    self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                    continue
                if self.exchange == "binance.com" \
                        or self.exchange == "binance.com-testnet" \
                        or self.exchange == "binance.us":
                    if int(stream_data['data']['u']) <= self.depth_caches[market]['last_update_id']:
                        # Drop it
                        logger.debug(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) "
                                     f"- Dropping outdated depth update of the cache with market {market}! Reason: "
                                     f"{stream_data['data']['u']} <= {self.depth_caches[market]['last_update_id']}")
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                    if int(stream_data['data']['U']) <= self.depth_caches[market]['last_update_id'] + 1 \
                            <= int(stream_data['data']['u']):
                        # The first processed event should have U <= lastUpdateId+1 AND u >= lastUpdateId+1.
                        self._apply_updates(asks=stream_data['data']['a'], bids=stream_data['data']['b'], market=market)
                        logger.info(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) -"
                                    f" Finished initialization of the cache with market {market} (Spot)")
                        # Init (refresh) finished
                        last_sync_time = time.time()
                        self.depth_caches[market]['last_update_id'] = int(stream_data['data']['u'])
                        self.depth_caches[market]['last_update_time'] = int(last_sync_time)
                        self.depth_caches[market]['last_refresh_time'] = int(last_sync_time)
                        self.depth_caches[market]['is_synchronized'] = True
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                elif self.exchange == "binance.com-futures" or self.exchange == "binance.com-futures-testnet":
                    if int(stream_data['data']['u']) < int(self.depth_caches[market]['last_update_id']):
                        # Drop it
                        logger.debug(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) -"
                                     f" Dropping outdated depth update of the cache with market {market}! Reason: "
                                     f"{stream_data['data']['u']} <= {self.depth_caches[market]['last_update_id']}")
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                    if int(stream_data['data']['U']) <= self.depth_caches[market]['last_update_id'] \
                            <= int(stream_data['data']['u']):
                        # The first processed event should have U <= lastUpdateId AND u >= lastUpdateId
                        self._apply_updates(asks=stream_data['data']['a'], bids=stream_data['data']['b'], market=market)
                        logger.info(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) - "
                                    f"Finished initialization of the cache with market {market} (Futures)")
                        # Init (refresh) finished
                        last_sync_time = time.time()
                        self.depth_caches[market]['last_update_id'] = int(stream_data['data']['u'])
                        self.depth_caches[market]['last_update_time'] = int(last_sync_time)
                        self.depth_caches[market]['is_synchronized'] = True
                        self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                        continue
                logger.info(f"BinanceLocalDepthCacheManager._manage_depth_cache_async(stream_id={stream_id}) - Set "
                            f"refresh_request for depth_cache with market {market}")
                self.depth_caches[market]['is_synchronized'] = False
                self.depth_caches[market]['refresh_request'] = True
                self.depth_caches[market]['last_update_id'] = None
                self.ubwa.asyncio_queue_task_done(stream_id=stream_id)
                continue

    def _process_stream_signals(self, signal_type=None, stream_id=None, data_record=None, error_msg=None) -> None:
        """
        Process stream_signals

        :return: None
        """
        logger.debug(f"BinanceLocalDepthCacheManager._process_stream_signals() - received stream_signal: "
                     f"{signal_type} - {stream_id} - {data_record} - {error_msg}")

        if signal_type == "CONNECT":
            logger.debug(f"BinanceLocalDepthCacheManager._process_stream_signals(stream_id={stream_id}) - Received "
                         f"stream_signal {signal_type} - Setting stream_status to `CONNECTED`")
            self.stream_status = "CONNECTED"
        elif signal_type == "DISCONNECT":
            logger.debug(f"BinanceLocalDepthCacheManager._process_stream_signals(stream_id={stream_id}) - Received "
                         f"stream_signal {signal_type} - Setting all caches to synchronized is False and triggering a "
                         f"refresh.")
            self.stream_status = "DISCONNECTED"
            if self.ubwa.is_stop_request(stream_id=stream_id) is False:
                self.ubwa.clear_asyncio_queue(stream_id=stream_id)
                logger.debug(f"BinanceLocalDepthCacheManager._process_stream_signals(stream_id={stream_id}) - AsyncIO "
                             f"Queue reset done!")
            for market in self.depth_caches:
                self.depth_caches[market]['is_synchronized'] = False
                self.depth_caches[market]['refresh_request'] = True
                self.depth_caches[market]['last_update_id'] = None
        elif signal_type == "FIRST_RECEIVED_DATA":
            logger.debug(f"BinanceLocalDepthCacheManager._process_stream_signals(stream_id={stream_id}) - Received "
                         f"stream_signal {signal_type} - Setting stream_status to `RUNNING`")
            self.stream_status = "RUNNING"
        elif signal_type == "STOP":
            logger.debug(f"BinanceLocalDepthCacheManager._process_stream_signals(stream_id={stream_id}) - Received "
                         f"stream_signal {signal_type} - Setting stream_status to `STOPPED`")
            self.stream_status = "STOPPED"
        else:
            logger.error(f"BinanceLocalDepthCacheManager._process_stream_signals(stream_id={stream_id}) - Received "
                         f"unexpected stream_signal {signal_type} - Setting stream_status to `{signal_type}`")
            self.stream_status = signal_type

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
    def _sort_depth_cache(items: dict,
                          limit_count: int = None,
                          reverse: bool = False,
                          threshold_volume: float = None) -> list:
        """
        Returns sorted asks or bids by price

        :param items: asks or bids
        :type items: dict
        :param limit_count: List elements threshold to trim the result.
        :type limit_count: int or None (0 is nothing, None is everything)
        :param reverse: False is regular, True is reversed
        :type reverse: bool
        :param threshold_volume: Volume threshold to trim the result
        :type threshold_volume: float
        :return: list
        """
        logger.debug(f"BinanceLocalDepthCacheManager._sort_depth_cache() - Start sorting ...")
        sorted_items = [[float(price), float(quantity)] for price, quantity in list(items.items())]
        sorted_items = sorted(sorted_items, key=itemgetter(0), reverse=reverse)
        if threshold_volume is None:
            return sorted_items[:limit_count]
        else:
            total_volume: float = 0.0
            trimmed_items: list = []
            for price, quantity in sorted_items:
                if (price * quantity) + total_volume <= threshold_volume or total_volume == 0.0:
                    trimmed_items.append([price, quantity])
                    total_volume += price * quantity
                else:
                    break
            return trimmed_items[:limit_count]

    def _subscribe_depth(self, markets: Optional[Union[str, list]] = None) -> bool:
        """
        Subscribe a market on a stream.

        :param markets: The markets
        :type markets: str or list
        :return: bool
        """
        if markets is None:
            return False
        if isinstance(markets, str):
            markets = [markets, ]
        if self.depth_cache_update_interval is None:
            channel = f"depth"
        else:
            channel = f"depth@{self.depth_cache_update_interval}ms"

        for market in markets:
            stream_id = self.get_stream_id()
            if stream_id is None:
                stream_id = self.ubwa.create_stream(channels=channel,
                                                    markets=market,
                                                    stream_label=f"ubldc_depth",
                                                    output="dict",
                                                    process_asyncio_queue=self._manage_depth_cache_async)
                uuid = self.ubwa.get_new_uuid_id()
                self.websockets[uuid] = {"id": uuid,
                                         "channel": channel,
                                         "markets": [market, ],
                                         "stream_id": stream_id}
            else:
                for ws_id in self.websockets:
                    if self.websockets[ws_id]['stream_id'] == stream_id:
                        self.websockets[ws_id]['markets'].append(market)
                        break
                self.ubwa.subscribe_to_stream(stream_id=stream_id, markets=market)

    def create_depthcache(self, markets: Union[str, List[str], None] = None, refresh_interval: int = None) -> bool:
        """
        Create one or more DepthCaches!

        :param markets: Specify the market symbols for caches to be created
        :type markets: str or list
        :param refresh_interval: The refresh interval in seconds, default is the `default_refresh_interval` of
                                 `BinanceLocalDepthCache <https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html?highlight=default_refresh_interval#unicorn_binance_local_depth_cache.manager.BinanceLocalDepthCacheManager>`__.
                                 The depth_cache is reset and reinitialized at this interval.
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

    def create_depth_cache(self, markets: Optional[str] = None, refresh_interval: int = None) -> bool:
        """
        ***Deprecated!*** Please use 'create_depthcache()' instead!
        """
        logger.warning(f"BinanceLocalDepthCacheManager.create_depth_cache() is deprecated, please use "
                       f"'create_depthcache()' instead!")
        return self.create_depthcache(markets=markets, refresh_interval=refresh_interval)

    def get_asks(self,
                 market: str = None,
                 limit_count: int = None,
                 threshold_volume: float = None) -> list:
        """
        Get the current list of asks with price and quantity.

        :param market: Specify the market symbol for the used depth_cache
        :type market: str
        :param limit_count: List elements threshold to trim the result.
        :type limit_count: int or None (0 is nothing, None is everything)
        :param threshold_volume: Volume threshold to trim the result.
        :type threshold_volume: float or None (0 is nothing, None is everything)
        :return: list
        """
        return self._get_book_side(market=market,
                                   limit_count=limit_count,
                                   reverse=False,
                                   side="asks",
                                   threshold_volume=threshold_volume)

    def get_bids(self,
                 market: str = None,
                 limit_count: int = None,
                 threshold_volume: float = None) -> list:
        """
        Get the current list of bids with price and quantity.

        :param market: Specify the market symbol for the used depth_cache.
        :type market: str
        :param limit_count: List elements threshold to trim the result.
        :type limit_count: int or None (0 is nothing, None is everything)
        :param threshold_volume: Volume threshold to trim the result.
        :type threshold_volume: float or None (0 is nothing, None is everything)
        :return: list
        """
        return self._get_book_side(market=market,
                                   limit_count=limit_count,
                                   reverse=True,
                                   side="bids",
                                   threshold_volume=threshold_volume)

    def _get_book_side(self,
                       market: str = None,
                       limit_count: int = None,
                       reverse: bool = False,
                       side: str = None,
                       threshold_volume: float = None) -> list:
        """
        Get the current list of bids with price and quantity.

        :param market: Specify the market symbol for the used depth_cache.
        :type market: str
        :param limit_count: List elements threshold to trim the result.
        :type limit_count: int or None (0 is nothing, None is everything)
        :param reverse: False is regular, True is reversed
        :type reverse: bool
        :param side: asks or bids
        :type side: str
        :param threshold_volume: Volume threshold to trim the result.
        :type threshold_volume: float or None (0 is nothing, None is everything)
        :return: list
        """
        if side is None:
            raise ValueError("Side must be specified.")
        if market is None:
            raise DepthCacheNotFound(market=market)
        market = market.lower()
        try:
            if self.is_depth_cache_synchronized(market=market) is False:
                raise DepthCacheOutOfSync(market=market)
        except KeyError:
            raise DepthCacheNotFound(market=market)
        try:
            if self.is_stop_request(market=market) is True:
                raise DepthCacheAlreadyStopped(market=market)
        except KeyError:
            raise DepthCacheNotFound(market=market)
        with self.threading_lock_bid[market]:
            return self._sort_depth_cache(items=self.depth_caches[market][side],
                                          limit_count=limit_count,
                                          reverse=reverse,
                                          threshold_volume=threshold_volume)

    @staticmethod
    def get_latest_release_info() -> Optional[dict]:
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

        :return: str or None
        """
        logger.debug(f"BinanceWebSocketApiManager.get_latest_version() - Started ...")
        # Do a fresh request if status is None or last timestamp is older 1 hour
        if self.last_update_check_github['status'].get('tag_name') is None or \
                (self.last_update_check_github['timestamp'] + (60 * 60) < time.time()):
            self.last_update_check_github['status'] = self.get_latest_release_info()
        if self.last_update_check_github['status'].get('tag_name') is not None:
            try:
                return self.last_update_check_github['status']['tag_name']
            except KeyError as error_msg:
                logger.debug(f"BinanceLocalDepthCacheManager.get_latest_version() - KeyError: {error_msg}")
                return None
        else:
            return None

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

    def get_ubra_manager(self) -> BinanceRestApiManager:
        """
        Get the used BinanceRestApiManager() instance of BinanceLocalDepthCacheManager()

        :return: BinanceRestApiManager
        """
        return self.ubra

    def get_ubwa_manager(self) -> BinanceWebSocketApiManager:
        """
        Get the used BinanceWebSocketApiManager() instance of BinanceLocalDepthCacheManager()

        :return: BinanceWebSocketApiManager
        """
        return self.ubwa

    def get_user_agent(self) -> str:
        """
        Get the user_agent string "lib name + lib version + python version"

        :return: str
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
        if market is None:
            logger.debug(f"BinanceLocalDepthCacheManager.is_depth_cache_synchronized() - Parameter `market` is "
                         f"mandatory!")
            raise DepthCacheNotFound(market=market)
        market = market.lower()
        try:
            status = self.depth_caches[market]['is_synchronized']
        except KeyError:
            raise DepthCacheNotFound(market=market)
        logger.debug(f"BinanceLocalDepthCacheManager.is_depth_cache_synchronized() - Returning the status: "
                     f"{status}")
        return status

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

    def get_stream_id(self, market: str = None) -> Optional[str]:
        """
        Get the stream_id of the corresponding stream.

        :return: stream_id (str) or None
        """
        if len(self.websockets) == 0:
            return None
        if market is not None:
            for ws_id in self.websockets:
                if market in self.websockets[ws_id]['markets']:
                    return self.websockets[ws_id]['stream_id']
        else:
            for ws_id in self.websockets:
                if self.ubwa.get_number_of_free_subscription_slots(stream_id=self.websockets[ws_id]['stream_id']) >= 1:
                    return self.websockets[ws_id]['stream_id']
            return None

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
        elif self.get_latest_version() is None:
            return False
        else:
            return True

    def get_version(self) -> str:
        """
        Get the package/module version

        :return: str
        """
        logger.debug(f"BinanceLocalDepthCacheManager.get_version() - Returning the version: {self.version}")
        return self.version

    def print_summary(self, add_string: str = None, footer: str = None, title: str = None) -> None:
        """
        Print an overview of all streams

        :param add_string: text to add to the output
        :type add_string: str
        :param footer: footer of the output
        :type footer: str
        :param title: title of the output
        :type title: str
        :return: None
        """
        if title is None:
            title = self.get_user_agent()
        else:
            if footer is None:
                footer = f"Powered by {self.get_user_agent()}"
        info = (f"update_interval_ms={self.depth_cache_update_interval}\r\n "
                f"binance_api_status={self.ubra.get_used_weight(cached=True)}")
        if add_string is not None:
            info = f"{info}\r\n {add_string}"
        self.ubwa.print_summary(add_string=info, footer=footer, title=title)

    def print_summary_to_png(self,
                             print_summary_export_path: str = None,
                             height_per_row: float = 12.5,
                             add_string: str = None,
                             footer: str = None,
                             title: str = None):
        """
        Create a PNG image file with the console output of `print_summary()`

        *LINUX ONLY* It should not be hard to make it OS independent:
        https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/issues/61

        :param print_summary_export_path: If you want to export the output of print_summary() to an image,
                                         please provide a path like "/var/www/html/". `View the Wiki!
                                         <https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/How-to-export-print_summary()-stdout-to-PNG%3F>`__
        :type print_summary_export_path: str
        :param height_per_row: set the height per row for the image height calculation
        :type height_per_row: float
        :param add_string: text to add to the output
        :type add_string: str
        :param footer: set a footer (last row) for print_summary output
        :type footer: str
        :param title: set a title (first row) for print_summary output
        :type title: str
        :return: bool
        """
        if title is None:
            title = self.get_user_agent()
        else:
            if footer is None:
                footer = f"Powered by {self.get_user_agent()}"
        info = (f"update_interval_ms={self.depth_cache_update_interval}\r\n "
                f"binance_api_status={self.ubra.get_used_weight(cached=True)}")
        if add_string is not None:
            info = f"{info}\r\n {add_string}"
        self.ubwa.print_summary_to_png(add_string=info,
                                       height_per_row=height_per_row,
                                       print_summary_export_path=print_summary_export_path,
                                       footer=footer,
                                       title=title)

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
            market = market.lower()
            logger.info(f"BinanceLocalDepthCacheManager.set_refresh_request() - Set refresh request for "
                        f"depth_cache {market}")
            self.depth_caches[market]['refresh_request'] = True
        return True

    def stop_depthcache(self, markets: Optional[Union[str, list]] = None) -> bool:
        """
        Stop and delete one or more DepthCaches!

        :param markets: Specify the market symbols for the depth_caches to be stopped and deleted
        :type markets: str or list
        :return: bool
        """
        if markets is None:
            logger.critical(f"BinanceLocalDepthCacheManager.stop_depthcache() - Please provide a market")
            return False
        if isinstance(markets, str):
            markets = [markets, ]
        for market in markets:
            market = market.lower()
            logger.info(f"BinanceLocalDepthCacheManager.stop_depthcache() - Setting stop_request for "
                        f"depth_cache `{market}`, stop its stream and clear the stream_buffer")
            try:
                self.depth_caches[market]['stop_request'] = True
            except KeyError:
                raise DepthCacheNotFound(market=market)
            stream_id = self.get_stream_id(market=market)
            if stream_id is not None:
                self.ubwa.unsubscribe_from_stream(stream_id=stream_id, markets=market)
        return True

    def stop_depth_cache(self, markets: Optional[Union[str, list]] = None) -> bool:
        """
        ***Deprecated!*** Please use 'stop_depthcache()' instead!
        """
        logger.warning(f"BinanceLocalDepthCacheManager.stop_depth_cache() is deprecated, please use "
                       f"'stop_depthcache()' instead!")
        return self.stop_depthcache(markets=markets)

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
