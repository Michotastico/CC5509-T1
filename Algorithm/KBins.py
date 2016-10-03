#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Michel Llorens"
__license__ = "GPL"
__version__ = "2.0.0"
__email__ = "mllorens@dcc.uchile.cl"


class K13Bins:
    def __init__(self):
        self.y_division = 3
        self.x_division = 2
        self.dictionary = dict()

    def classify_division(self, image):
        """Return a classification vector of a binary image"""
        height, width = image.shape
        divisions = self.divide_image(height, width)
        concatenated_histogram = []
        for init_tuple, end_tuple in divisions:
            histogram = self.generate_histogram(image, init_tuple[0], init_tuple[1], end_tuple[0],
                                                end_tuple[1], height, width)
            concatenated_histogram += histogram
        return concatenated_histogram

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

    def generate_histogram(self, image, init_x, init_y, end_x, end_y, height, width):
        histogram = [0]*13
        for x_index in range(init_x, end_x + 1):
            for y_index in range(init_y, end_y + 1):
                total = 0
                if image[y_index, x_index] == 0:
                    continue

                hist_0 = hist_1 = hist_2 = hist_3 = 0

                if 0 in image[y_index, x_index + 1:]:
                    hist_1 += 1
                if 0 in image[y_index, : x_index]:
                    hist_3 += 1
                if 0 in image[y_index + 1:, x_index]:
                    hist_2 += 1
                if 0 in image[: y_index, x_index]:
                    hist_0 += 1

                total = hist_0 + hist_1 + hist_2 + hist_3
                if total < 2:
                    continue
                elif total == 2:
                    if hist_0 == 0 and hist_1 == 0:
                        histogram[0] += 1
                    elif hist_1 == 0 and hist_2 == 0:
                        histogram[1] += 1
                    elif hist_2 == 0 and hist_3 == 0:
                        histogram[2] += 1
                    elif hist_3 == 0 and hist_0 == 0:
                        histogram[3] += 1
                elif total == 3:
                    if hist_0 == 0 and hist_1 == 0:
                        histogram[4] += 1
                    elif hist_1 == 0 and hist_2 == 0:
                        histogram[5] += 1
                    elif hist_2 == 0 and hist_3 == 0:
                        histogram[6] += 1
                    elif hist_3 == 0 and hist_0 == 0:
                        histogram[7] += 1
                else:
                    hist_x_1 = hist_x_2 = hist_x_3 = hist_x_4 = 0

                    # diag 1
                    curr_x = x_index - 1
                    curr_y = y_index - 1

                    while curr_x >= 0 and curr_y >= 0:
                        if image[curr_y, curr_x] == 0:
                            hist_x_1 += 1
                            break
                        curr_x -= 1
                        curr_y -= 1

                    # diag 4
                    curr_x = x_index + 1
                    curr_y = y_index + 1

                    while curr_x < width and curr_y < height:
                        if image[curr_y, curr_x] == 0:
                            hist_x_4 += 1
                            break
                        curr_x += 1
                        curr_y += 1

                    # diag 2
                    curr_x = x_index + 1
                    curr_y = y_index - 1

                    while curr_x < width and curr_y >= 0:
                        if image[curr_y, curr_x] == 0:
                            hist_x_2 += 1
                            break
                        curr_x += 1
                        curr_y -= 1

                    # diag 3
                    curr_x = x_index - 1
                    curr_y = y_index + 1

                    while curr_y < height and curr_x >= 0:
                        if image[curr_y, curr_x] == 0:
                            hist_x_3 += 1
                            break
                        curr_x -= 1
                        curr_y += 1

                    total_x = hist_x_1 + hist_x_2 + hist_x_3 + hist_x_4

                    if total_x == 4:
                        histogram[8] += 1
                    elif hist_x_1 == 0:
                        histogram[9] += 1
                    elif hist_x_2 == 0:
                        histogram[10] += 1
                    elif hist_x_3 == 0:
                        histogram[11] += 1
                    elif hist_x_4 == 0:
                        histogram[12] += 1
        return histogram
