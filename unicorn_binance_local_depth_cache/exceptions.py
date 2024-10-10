#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: unicorn_binance_local_depth_cache/exceptions.py
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


class DepthCacheClusterNotReachableError(Exception):
    """
    Exception raised when the UBDCC is not reachable.
    """
    def __init__(self, url=None):
        if url is None:
            self.message = f"Connection with UBDCC could not be established!"
        else:
            self.message = f"Connection with UBDCC ({url}) could not be established!"
        super().__init__(self.message)


class DepthCacheOutOfSync(Exception):
    """
    Exception raised when an attempt is made to use a depth_cache that is out of sync.
    """
    def __init__(self, market=None):
        if market is None:
            self.message = f"The depth_cache is out of sync, please try again later"
        else:
            self.message = f"The depth_cache for market '{market}' is out of sync, please try again later"
        super().__init__(self.message)


class DepthCacheAlreadyStopped(Exception):
    """
    Exception raised when an attempt is made to use a depth_cache that has already been stopped.
    """
    def __init__(self, market=None):
        if market is None:
            self.message = f"The depth_cache is already stopped!"
        else:
            self.message = f"The depth_cache for market '{market}' is already stopped!"
        super().__init__(self.message)


class DepthCacheNotFound(Exception):
    """
    Exception raised when an attempt is made to use an instance that does not exist.
    """
    def __init__(self, market=None):
        if market is None:
            self.message = f"The depth_cache does not exist!"
        else:
            self.message = f"The depth_cache for market '{market}' does not exist!"
        super().__init__(self.message)
