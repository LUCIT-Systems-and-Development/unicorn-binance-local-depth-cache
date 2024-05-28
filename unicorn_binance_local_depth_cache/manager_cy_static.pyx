# cython: language_level=3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: unicorn_binance_local_depth_cache/manager_cy.pyx
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

from operator import itemgetter
import cython
import logging
from libc.stdlib cimport malloc, free

__logger__: logging.Logger = logging.getLogger("unicorn_binance_local_depth_cache")
logger = __logger__

@cython.ccall
@cython.nogil
def _sort_depth_cache(double[:, ::1] items,
                      cython.bint reverse = False,
                      cython.double threshold_volume = -1.0) -> list:
    """
    Returns sorted asks or bids by price

    :param items: asks or bids
    :type items: double[:, ::1]
    :param reverse: False is regular, True is reversed
    :type reverse: bool
    :param threshold_volume: Volume threshold to trim the result
    :type threshold_volume: float
    :return: list
    """
    cdef int i, j, n = items.shape[0]
    cdef double total_volume = 0.0
    cdef double[:, ::1] sorted_items
    cdef double[:, ::1] trimmed_items
    cdef double[:] temp

    # Allocate memory for sorted_items and trimmed_items
    sorted_items = <double[:, ::1]>malloc(n * 2 * cython.sizeof(double))
    trimmed_items = <double[:, ::1]>malloc(n * 2 * cython.sizeof(double))

    if not sorted_items or not trimmed_items:
        if sorted_items:
            free(sorted_items)
        if trimmed_items:
            free(trimmed_items)
        raise MemoryError()

    # Copy and sort the items
    with cython.gil:
        for i in range(n):
            sorted_items[i, 0] = items[i, 0]
            sorted_items[i, 1] = items[i, 1]
        sorted_items[:n] = sorted(sorted_items[:n], key=itemgetter(0), reverse=reverse)

    # If no threshold volume is given, return the sorted items
    if threshold_volume < 0:
        result = []
        with cython.gil:
            for i in range(n):
                result.append([sorted_items[i, 0], sorted_items[i, 1]])
        free(sorted_items)
        free(trimmed_items)
        return result

    # Apply the threshold volume
    j = 0
    for i in range(n):
        price = sorted_items[i, 0]
        quantity = sorted_items[i, 1]
        if (price * quantity) + total_volume <= threshold_volume or total_volume == 0.0:
            trimmed_items[j, 0] = price
            trimmed_items[j, 1] = quantity
            total_volume += price * quantity
            j += 1
        else:
            break

    # Convert the result to a Python list
    result = []
    with cython.gil:
        for i in range(j):
            result.append([trimmed_items[i, 0], trimmed_items[i, 1]])

    free(sorted_items)
    free(trimmed_items)
    return result

def sort_depth_cache_wrapper(items: dict,
                             limit_count: int = None,
                             reverse: bool = False,
                             threshold_volume: float = None) -> list:
    cdef int n = len(items)
    cdef double[:, ::1] c_items = <double[:n, 2]>malloc(n * 2 * cython.sizeof(double))

    if not c_items:
        raise MemoryError()

    with cython.gil:
        i = 0
        for k, v in items.items():
            c_items[i, 0] = float(k)
            c_items[i, 1] = float(v)
            i += 1

    sorted_items = _sort_depth_cache(c_items,
                                     reverse=reverse,
                                     threshold_volume=threshold_volume if threshold_volume is not None else -1)

    free(c_items)

    if limit_count is None:
        return sorted_items
    return sorted_items[:limit_count]
