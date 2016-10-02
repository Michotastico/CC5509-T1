#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Algorithm.KBins import K13Bins

__author__ = "Michel Llorens"
__license__ = "GPL"
__version__ = "2.0.0"
__email__ = "mllorens@dcc.uchile.cl"

bins = K13Bins(3, 3)
bins.classify_without_division('hola')
