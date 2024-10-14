#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: unicorn_binance_local_depth_cache/cluster.py
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

import logging
import json
import requests
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
        if self.test():
            logger.info(f"Connection with UBDCC {self.url} successfully established! Activate cluster mode ...")
        else:
            raise DepthCacheClusterNotReachableError(url=self.url)

    def _build_url(self) -> None:
        protocol = "http"
        if self.port == 80 or self.port is None:
            self.url = f"{protocol}://{self.address}/"
        else:
            self.url = f"{protocol}://{self.address}:{self.port}/"

    def _request(self, endpoint, method, params=None, headers=None, timeout=10) -> dict:
        try:
            if method == "get":
                response = requests.get(self.url+endpoint, params=params, headers=headers, timeout=timeout)
            elif method == "post":
                response = requests.post(self.url+endpoint, json=json.dumps(params),
                                         headers={"Content-Type": "application/json"})
            else:
                raise ValueError("Allowed 'method' values: get, post")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error_msg:
            print(f"An error occurred: {error_msg}")
            return {"error": error_msg}

    def create_depthcache(self,
                          exchange: str = None,
                          market: str = None,
                          desired_quantity: int = None,
                          update_interval: int = None,
                          refresh_interval: int = None):
        if exchange is None or market is None:
            raise ValueError("Missing mandatory parameter: exchange, market")
        params = {"exchange": exchange,
                  "market": market,
                  "desired_quantity": desired_quantity,
                  "update_interval": update_interval,
                  "refresh_interval": refresh_interval}
        return self._request(self.endpoints.create_depthcache, method="get", params=params)

    def get_asks(self,
                 exchange: str = None,
                 market: str = None,
                 limit_count: int = None,
                 threshold_volume: int = None):
        if exchange is None or market is None:
            raise ValueError("Missing mandatory parameter: exchange, market")
        params = {"exchange": exchange,
                  "market": market,
                  "limit_count": limit_count,
                  "threshold_volume": threshold_volume}
        return self._request(self.endpoints.get_asks, method="get", params=params)

    def get_bids(self,
                 exchange: str = None,
                 market: str = None,
                 limit_count: int = None,
                 threshold_volume: int = None):
        if exchange is None or market is None:
            raise ValueError("Missing mandatory parameter: exchange, market")
        params = {"exchange": exchange,
                  "market": market,
                  "limit_count": limit_count,
                  "threshold_volume": threshold_volume}
        return self._request(self.endpoints.get_bids, method="get", params=params)

    def get_cluster_info(self):
        return self._request(self.endpoints.get_cluster_info, method="get")

    def get_depthcache_list(self):
        return self._request(self.endpoints.get_depthcache_list, method="get")

    def get_depthcache_info(self, exchange: str = None, market: str = None):
        if exchange is None or market is None:
            raise ValueError("Missing mandatory parameter: exchange, market")
        params = {"exchange": exchange,
                  "market": market}
        return self._request(self.endpoints.get_depthcache_info, method="get", params=params)

    def get_test(self):
        return self._request(self.endpoints.test, method="get")

    def submit_license(self, api_secret: str = None, license_token: str = None):
        if api_secret is None or license_token is None:
            raise ValueError("Missing mandatory parameter: api_secret, license_token")
        params = {"api_secret": api_secret,
                  "license_token": license_token}
        return self._request(self.endpoints.submit_license, method="get", params=params)

    def stop_depthcache(self, exchange: str = None, market: str = None):
        if exchange is None or market is None:
            raise ValueError("Missing mandatory parameter: exchange, market")
        params = {"exchange": exchange,
                  "market": market}
        return self._request(self.endpoints.stop_depthcache, method="get", params=params)

    def test(self):
        test = self._request(self.endpoints.test, method="get")
        if test.get('app') is not None and test.get('result') is not None:
            if test['app']['name'] == "lucit-ubdcc-restapi" and test['result'] == "OK":
                return True
        return False
