#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: unicorn_binance_local_depth_cache/cluster.py
#
# Part of ‘UNICORN Binance Local Depth Cache’
# Project website: https://github.com/oliver-zehentleitner/unicorn-binance-local-depth-cache
# Github: https://github.com/oliver-zehentleitner/unicorn-binance-local-depth-cache
# Documentation: https://oliver-zehentleitner.github.io/unicorn-binance-local-depth-cache
# PyPI: https://pypi.org/project/unicorn-binance-local-depth-cache
#
# License: MIT
# https://github.com/oliver-zehentleitner/unicorn-binance-local-depth-cache/blob/master/LICENSE
#
# Author: Oliver Zehentleitner
#
# Copyright (c) 2019-2026, Oliver Zehentleitner (https://about.me/oliver-zehentleitner)
#
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

import aiohttp
import asyncio
import logging
import orjson as json
import requests
import time
from .cluster_endpoints import ClusterEndpoints
from .exceptions import DepthCacheClusterNotReachableError

__logger__: logging.getLogger = logging.getLogger("unicorn_binance_local_depth_cache")
logger = __logger__


class Cluster:
    def __init__(self, address: str = None, port: int = None):
        self.address: str = address
        self.endpoints: ClusterEndpoints = ClusterEndpoints()
        self.port: int = port
        self.url: str
        self._build_url()
        if self.test_connection():
            logger.info(
                f"Connection with UBDCC {self.url} successfully established! Activate cluster mode ..."
            )
        else:
            raise DepthCacheClusterNotReachableError(url=self.url)

    def _build_url(self) -> None:
        protocol = "http"
        if self.port == 80 or self.port is None:
            self.url = f"{protocol}://{self.address}/"
        else:
            self.url = f"{protocol}://{self.address}:{self.port}/"

    def _request(
        self,
        endpoint: str,
        method: str,
        params: dict = None,
        headers: dict = None,
        timeout: int = 10,
        debug: bool = False,
    ) -> dict:
        start_time: float = 0.0
        if debug is True:
            start_time = time.time()
            if params is None:
                params = {"debug": "true"}
            else:
                params.update({"debug": "true"})
        try:
            if method == "get":
                response = requests.get(
                    self.url + endpoint, params=params, headers=headers, timeout=timeout
                )
            elif method == "post":
                response = requests.post(self.url + endpoint, json=params)
            else:
                raise ValueError("Allowed 'method' values: get, post")
            response.raise_for_status()
            result = response.json()
            if debug is True and result.get("debug") is not None:
                request_time = time.time() - start_time
                result["debug"]["request_time"] = request_time
                result["debug"]["transmission_time"] = (
                    request_time - result["debug"]["cluster_execution_time"]
                )
            return result
        except requests.exceptions.RequestException as error_msg:
            logger.error(f"Cluster._request() - {self.url+endpoint} - {error_msg}")
            return {"error": error_msg}

    async def _request_async(
        self,
        endpoint: str,
        method: str,
        params: dict = None,
        headers: dict = None,
        timeout: int = 10,
        debug: bool = False,
    ) -> dict:
        start_time: float = 0.0
        if params is not None:
            params = {k: v for k, v in params.items() if v is not None}
        if debug is True:
            start_time = time.time()
            if params is None:
                params = {"debug": "true"}
            else:
                params.update({"debug": "true"})
        try:
            async with aiohttp.ClientSession() as session:
                if method == "get":
                    async with session.get(
                        self.url + endpoint,
                        params=params,
                        headers=headers,
                        timeout=timeout,
                    ) as response:
                        response.raise_for_status()
                        result = await response.json()
                elif method == "post":
                    async with session.post(
                        self.url + endpoint,
                        json=params,
                        headers={"Content-Type": "application/json"},
                        timeout=timeout,
                    ) as response:
                        response.raise_for_status()
                        result = await response.json()
                else:
                    raise ValueError("Allowed 'method' values: get, post")
            if debug is True and result.get("debug") is not None:
                request_time = time.time() - start_time
                result["debug"]["request_time"] = request_time
                result["debug"]["transmission_time"] = (
                    request_time - result["debug"]["cluster_execution_time"]
                )
            return result
        except asyncio.CancelledError as error_msg:
            logger.warning(
                f"Cluster._request_async() - asyncio.CancelledError - {self.url+endpoint} - {error_msg}"
            )
            return {
                "error": f"asyncio.CancelledError - {self.url+endpoint} - {str(error_msg)}"
            }
        except asyncio.TimeoutError:
            logger.warning(
                f"Cluster._request_async() - asyncio.TimeoutError - {self.url+endpoint}"
            )
            return {"error": f"asyncio.TimeoutError - {self.url+endpoint}"}
        except aiohttp.ClientError as error_msg:
            logger.error(
                f"Cluster._request_async() - aiohttp.ClientError - {self.url+endpoint} - {error_msg}"
            )
            return {
                "error": f"aiohttp.ClientError - {self.url+endpoint} - {str(error_msg)}"
            }

    def create_depthcache(
        self,
        exchange: str = None,
        market: str = None,
        desired_quantity: int = None,
        update_interval: int = None,
        refresh_interval: int = None,
        debug: bool = False,
    ) -> dict:
        if exchange is None or market is None:
            raise ValueError("Missing mandatory parameter: exchange, market")
        params = {
            "exchange": exchange,
            "market": market,
            "desired_quantity": desired_quantity,
            "update_interval": update_interval,
            "refresh_interval": refresh_interval,
        }
        return self._request(
            self.endpoints.create_depthcache, method="get", params=params, debug=debug
        )

    async def create_depthcache_async(
        self,
        exchange: str = None,
        market: str = None,
        desired_quantity: int = None,
        update_interval: int = None,
        refresh_interval: int = None,
        debug: bool = False,
    ) -> dict:
        if exchange is None or market is None:
            raise ValueError("Missing mandatory parameter: exchange, market")
        params = {
            "exchange": exchange,
            "market": market,
            "desired_quantity": desired_quantity,
            "update_interval": update_interval,
            "refresh_interval": refresh_interval,
        }
        return await self._request_async(
            self.endpoints.create_depthcache, method="get", params=params, debug=debug
        )

    def create_depthcaches(
        self,
        exchange: str = None,
        markets: list = None,
        desired_quantity: int = None,
        update_interval: int = None,
        refresh_interval: int = None,
        debug: bool = False,
    ) -> dict:
        if exchange is None or markets is None:
            raise ValueError("Missing mandatory parameter: exchange, markets")
        params = {
            "exchange": exchange,
            "markets": markets,
            "desired_quantity": desired_quantity,
            "update_interval": update_interval,
            "refresh_interval": refresh_interval,
        }
        return self._request(
            self.endpoints.create_depthcaches, method="post", params=params, debug=debug
        )

    async def create_depthcaches_async(
        self,
        exchange: str = None,
        markets: list = None,
        desired_quantity: int = None,
        update_interval: int = None,
        refresh_interval: int = None,
        debug: bool = False,
    ) -> dict:
        if exchange is None or markets is None:
            raise ValueError("Missing mandatory parameter: exchange, markets")
        params = {
            "exchange": exchange,
            "markets": markets,
            "desired_quantity": desired_quantity,
            "update_interval": update_interval,
            "refresh_interval": refresh_interval,
        }
        return await self._request_async(
            self.endpoints.create_depthcaches, method="post", params=params, debug=debug
        )

    def get_asks(
        self,
        exchange: str = None,
        market: str = None,
        limit_count: int = None,
        threshold_volume: int = None,
        debug: bool = False,
    ) -> dict:
        if exchange is None or market is None:
            raise ValueError("Missing mandatory parameter: exchange, market")
        params = {
            "exchange": exchange,
            "market": market,
            "limit_count": limit_count,
            "threshold_volume": threshold_volume,
        }
        return self._request(
            self.endpoints.get_asks, method="get", params=params, debug=debug
        )

    async def get_asks_async(
        self,
        exchange: str = None,
        market: str = None,
        limit_count: int = None,
        threshold_volume: int = None,
        debug: bool = False,
    ) -> dict:
        if exchange is None or market is None:
            raise ValueError("Missing mandatory parameter: exchange, market")
        params = {
            "exchange": exchange,
            "market": market,
            "limit_count": limit_count,
            "threshold_volume": threshold_volume,
        }
        return await self._request_async(
            self.endpoints.get_asks, method="get", params=params, debug=debug
        )

    def get_bids(
        self,
        exchange: str = None,
        market: str = None,
        limit_count: int = None,
        threshold_volume: int = None,
        debug: bool = False,
    ) -> dict:
        if exchange is None or market is None:
            raise ValueError("Missing mandatory parameter: exchange, market")
        params = {
            "exchange": exchange,
            "market": market,
            "limit_count": limit_count,
            "threshold_volume": threshold_volume,
        }
        return self._request(
            self.endpoints.get_bids, method="get", params=params, debug=debug
        )

    async def get_bids_async(
        self,
        exchange: str = None,
        market: str = None,
        limit_count: int = None,
        threshold_volume: int = None,
        debug: bool = False,
    ) -> dict:
        if exchange is None or market is None:
            raise ValueError("Missing mandatory parameter: exchange, market")
        params = {
            "exchange": exchange,
            "market": market,
            "limit_count": limit_count,
            "threshold_volume": threshold_volume,
        }
        return await self._request_async(
            self.endpoints.get_bids, method="get", params=params, debug=debug
        )

    def get_cluster_info(self, debug: bool = False) -> dict:
        return self._request(self.endpoints.get_cluster_info, method="get", debug=debug)

    async def get_cluster_info_async(self, debug: bool = False) -> dict:
        return await self._request_async(
            self.endpoints.get_cluster_info, method="get", debug=debug
        )

    def get_depthcache_list(self, debug: bool = False) -> dict:
        return self._request(
            self.endpoints.get_depthcache_list, method="get", debug=debug
        )

    async def get_depthcache_list_async(self, debug: bool = False) -> dict:
        return await self._request_async(
            self.endpoints.get_depthcache_list, method="get", debug=debug
        )

    def get_depthcache_info(
        self, exchange: str = None, market: str = None, debug: bool = False
    ) -> dict:
        if exchange is None or market is None:
            raise ValueError("Missing mandatory parameter: exchange, market")
        params = {"exchange": exchange, "market": market}
        return self._request(
            self.endpoints.get_depthcache_info, method="get", params=params, debug=debug
        )

    async def get_depthcache_info_async(
        self, exchange: str = None, market: str = None, debug: bool = False
    ) -> dict:
        if exchange is None or market is None:
            raise ValueError("Missing mandatory parameter: exchange, market")
        params = {"exchange": exchange, "market": market}
        return await self._request_async(
            self.endpoints.get_depthcache_info, method="get", params=params, debug=debug
        )

    def get_test(self) -> dict:
        return self._request(self.endpoints.test, method="get")

    async def get_test_async(self) -> dict:
        return await self._request_async(self.endpoints.test, method="get")

    def stop_depthcache(
        self, exchange: str = None, market: str = None, debug: bool = False
    ) -> dict:
        if exchange is None or market is None:
            raise ValueError("Missing mandatory parameter: exchange, market")
        params = {"exchange": exchange, "market": market}
        return self._request(
            self.endpoints.stop_depthcache, method="get", params=params, debug=debug
        )

    async def stop_depthcache_async(
        self, exchange: str = None, market: str = None, debug: bool = False
    ) -> dict:
        if exchange is None or market is None:
            raise ValueError("Missing mandatory parameter: exchange, market")
        params = {"exchange": exchange, "market": market}
        return await self._request_async(
            self.endpoints.stop_depthcache, method="get", params=params, debug=debug
        )

    def add_credentials(
        self,
        account_group: str = None,
        api_key: str = None,
        api_secret: str = None,
        debug: bool = False,
    ) -> dict:
        """Store a Binance API key pair in the cluster for a given account group
        (binance.com, binance.com-testnet, binance.com-futures-testnet,
        binance.us, binance.tr). Multiple pairs per group are allowed and get
        load-balanced across DCNs. Returns the generated credential id."""
        if account_group is None or api_key is None or api_secret is None:
            raise ValueError(
                "Missing mandatory parameter: account_group, api_key, api_secret"
            )
        params = {
            "account_group": account_group,
            "api_key": api_key,
            "api_secret": api_secret,
        }
        return self._request(
            self.endpoints.add_credentials, method="post", params=params, debug=debug
        )

    async def add_credentials_async(
        self,
        account_group: str = None,
        api_key: str = None,
        api_secret: str = None,
        debug: bool = False,
    ) -> dict:
        if account_group is None or api_key is None or api_secret is None:
            raise ValueError(
                "Missing mandatory parameter: account_group, api_key, api_secret"
            )
        params = {
            "account_group": account_group,
            "api_key": api_key,
            "api_secret": api_secret,
        }
        return await self._request_async(
            self.endpoints.add_credentials, method="post", params=params, debug=debug
        )

    def remove_credentials(
        self, credential_id: str = None, debug: bool = False
    ) -> dict:
        """Remove a stored API key pair by id."""
        if credential_id is None:
            raise ValueError("Missing mandatory parameter: credential_id")
        params = {"id": credential_id}
        return self._request(
            self.endpoints.remove_credentials, method="post", params=params, debug=debug
        )

    async def remove_credentials_async(
        self, credential_id: str = None, debug: bool = False
    ) -> dict:
        if credential_id is None:
            raise ValueError("Missing mandatory parameter: credential_id")
        params = {"id": credential_id}
        return await self._request_async(
            self.endpoints.remove_credentials, method="post", params=params, debug=debug
        )

    def get_credentials_list(self, debug: bool = False) -> dict:
        """List stored credentials. API keys are returned masked (preview only);
        api_secret is never returned. Each entry lists the DCN UIDs it is
        currently assigned to."""
        return self._request(
            self.endpoints.get_credentials_list, method="get", debug=debug
        )

    async def get_credentials_list_async(self, debug: bool = False) -> dict:
        return await self._request_async(
            self.endpoints.get_credentials_list, method="get", debug=debug
        )

    def test_connection(self) -> bool:
        test = self._request(self.endpoints.test, method="get")
        if test.get("app") is not None and test.get("result") is not None:
            if test["app"]["name"] == "ubdcc-restapi" and test["result"] == "OK":
                return True
        return False

    async def test_connection_async(self) -> bool:
        test = await self._request_async(self.endpoints.test, method="get")
        if test.get("app") is not None and test.get("result") is not None:
            if test["app"]["name"] == "ubdcc-restapi" and test["result"] == "OK":
                return True
        return False
