#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Michel Llorens"
__license__ = "GPL"
__version__ = "2.0.0"
__email__ = "mllorens@dcc.uchile.cl"


class K13Bins:
    def __init__(self, y_division, x_division):
        self.y_division = y_division
        self.x_division = x_division
        self.dictionary = dict()

    def classify_without_division(self, image):
        """Return a classification vector of a binary image"""
        #height, width = image.shape
        height = 36
        width = 30
        divisions = self.divide_image(height, width)
        for init_tuple, end_tuple in divisions:
            print init_tuple, end_tuple
            for x_index in range(init_tuple[0], end_tuple[0] + 1):
                for y_index in range(init_tuple[1], end_tuple[1] + 1):
                    c = 1

    def divide_image(self, height, width):
        key = str(height) + str(width)
        if key not in self.dictionary:
            x_index = 0
            x_block = width/self.x_division
            x_blocks = []
            for i in range(self.x_division - 1):
                x_blocks.append(x_index)
                x_index += x_block
            x_blocks.append(x_index)

            y_index = 0
            y_block = height/self.y_division
            y_blocks = []
            for i in range(self.y_division - 1):
                y_blocks.append(y_index)
                y_index += y_block
            y_blocks.append(y_index)

            divisions = []

            x_index = 0
            y_index = 0
            # For first col
            init_tuple = (x_blocks[x_index], y_blocks[y_index])
            end_tuple = (x_blocks[x_index + 1], y_blocks[y_index + 1])
            divisions.append((init_tuple, end_tuple))
            for y_index in range(1, len(y_blocks) - 1):
                init_tuple = (x_blocks[x_index], y_blocks[y_index] + 1)
                end_tuple = (x_blocks[x_index + 1], y_blocks[y_index + 1])
                divisions.append((init_tuple, end_tuple))
            init_tuple = (x_blocks[x_index], y_blocks[len(y_blocks) - 1] + 1)
            end_tuple = (x_blocks[x_index + 1], height - 1)
            divisions.append((init_tuple, end_tuple))

            # For middle cols
            for x_index in range(1, len(x_blocks) - 1):
                y_index = 0
                init_tuple = (x_blocks[x_index] + 1, y_blocks[y_index])
                end_tuple = (x_blocks[x_index + 1], y_blocks[y_index + 1])
                divisions.append((init_tuple, end_tuple))
                for y_index in range(1, len(y_blocks) - 1):
                    init_tuple = (x_blocks[x_index] + 1, y_blocks[y_index] + 1)
                    end_tuple = (x_blocks[x_index + 1], y_blocks[y_index + 1])
                    divisions.append((init_tuple, end_tuple))
                init_tuple = (x_blocks[x_index] + 1, y_blocks[len(y_blocks) - 1])
                end_tuple = (x_blocks[x_index + 1], height - 1)
                divisions.append((init_tuple, end_tuple))

            # For last col
            x_index = len(x_blocks) - 1
            y_index = 0
            init_tuple = (x_blocks[x_index] + 1, y_blocks[y_index])
            end_tuple = (width - 1, y_blocks[y_index + 1])
            divisions.append((init_tuple, end_tuple))
            for y_index in range(1,len(y_blocks) - 1):
                init_tuple = (x_blocks[x_index] + 1, y_blocks[y_index] + 1)
                end_tuple = (width - 1, y_blocks[y_index + 1])
                divisions.append((init_tuple, end_tuple))
            init_tuple = (x_blocks[x_index] + 1, y_blocks[len(y_blocks) - 1] + 1)
            end_tuple = (width - 1, height - 1)
            divisions.append((init_tuple, end_tuple))

            self.dictionary[key] = divisions

        return self.dictionary[key]
