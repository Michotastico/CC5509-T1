#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Algorithm.KBins import K13Bins
from skimage import io, color
import numpy as np
import cv2

__author__ = "Michel Llorens"
__license__ = "GPL"
__version__ = "2.0.0"
__email__ = "mllorens@dcc.uchile.cl"

bins = K13Bins()
image = cv2.imread('Images/Images_CVL/test/0-0246-03-04.png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
ret, black_white = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

print bins.classify_division(black_white)
