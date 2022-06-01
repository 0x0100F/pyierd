#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""pyierdYLIARD - Kraken Exchange API client.

This is a REST API client module which allows you to query the API endpoints of
the Kraken exchange. It can make public and private domain queries. In case of
private queries an API key is required. The key can be loaded from a file or
provided as a string.

https://docs.kraken.com/rest/
https://github.com/0x0100F/pyierd
"""

from . import version

__author__ = "0x0100F"
__version__ = version.__version__
__license__ = "Apache-2.0"
