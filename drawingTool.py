import abc
import argparse
import os.path
from os import path
from typing import Optional

import numpy as np


class Canvas:
    def __init__(self, canvas):
        self.canvas_det = canvas
        self.canvas = [[' ' for x in range(int(self.canvas_det[1]))] for y in range(int(self.canvas_det[2]))]


class Shape:
    __metaclass__ = abc.ABCMeta

    def __init__(self, points, canvas):
        self.p1, self.p2 = points
        self.x1, self.y1 = self.p1
        self.x2, self.y2 = self.p2
        self.canvas = canvas

    @staticmethod
    def range_correction(a: int, b: int):
        if a < b:
            line = (a - 1, b)
        else:
            line = (b - 1, a)
        return line

    @abc.abstractmethod
    def draw(self):
        pass


class Line(Shape):

    def draw(self) -> None:
        if self.x1 == self.x2:
            x = self.x1 - 1
            line = self.range_correction(self.y1, self.y2)
            for i in range(*line):
                self.canvas.canvas[i][x] = 'x'
        # draw horizontal line
        elif self.y2 == self.y2:
            y = self.y1 - 1
            line = self.range_correction(self.x1, self.x2)
            for i in range(*line):
                self.canvas.canvas[y][i] = 'x'
        else:
            print('Not valid coordinates to plot a horizontal/vertical line')


class Rectangle(Shape):

    def draw(self) -> None:
        p1_p = (self.x2, self.y1)
        p2_p = (self.x1, self.y2)
        # draw_horizontal_lines
        line_h1 = Line((self.p1, p1_p), self.canvas)
        line_h1.draw()
        line_h2 = Line((p2_p, self.p2), self.canvas)
        line_h2.draw()
        # draw_vertical_lines
        line_v1 = Line((self.p1, p2_p), self.canvas)
        line_v1.draw()
        line_v2 = Line((p1_p, self.p2), self.canvas)
        line_v2.draw()


class Drawer:

    def __init__(self, canvas: list, instructions: list):
        self.cv = Canvas(canvas)
        self.instructions = instructions

    def bucket_fill(self, start_coords: tuple, fill_value: str) -> None:
        """
    Flood fill algorithm

    Parameters
    ----------
    data : (M, N) ndarray of uint8 type
        Image with flood to be filled. Modified inplace.
    start_coords : tuple
        Length-2 tuple of ints defining (row, col) start coordinates.
    fill_value : int
        Value the flooded area will take after the fill.

    Returns
    -------
    None, ``data`` is modified inplace.
    """
        xsize = len(self.cv.canvas[0])
        ysize = len(self.cv.canvas)
        orig_value = self.cv.canvas[start_coords[1]][start_coords[0]]

        stack = set(((start_coords[0], start_coords[1]),))
        if fill_value == orig_value:
            raise ValueError("Filling region with same value "
                             "already present is unsupported. "
                             "Did you already fill this region?")

        while stack:
            x, y = stack.pop()

            if self.cv.canvas[y][x] == orig_value:
                self.cv.canvas[y][x] = fill_value
                if x > 0:
                    stack.add((x - 1, y))
                if x < (xsize - 1):
                    stack.add((x + 1, y))
                if y > 0:
                    stack.add((x, y - 1))
                if y < (ysize - 1):
                    stack.add((x, y + 1))

    def graph(self) -> Optional[None]:
        # for step in list_steps:
        for instruction in self.instructions:
            # Draw Line
            if instruction[0] == 'L':
                if len(instruction) == 5:
                    try:
                        p1 = (int(instruction[1]), int(instruction[2]))
                        p2 = (int(instruction[3]), int(instruction[4]))
                        line_obj = Line((p1, p2), self.cv)
                        line_obj.draw()
                        # self.draw_canvas()
                        # self.draw_line((p1, p2))
                        self.graph_canvas()
                    except ValueError:
                        print('Invalid line arguments')
                else:
                    print('invalid number of arguments for Draw line')
                    return
            # Draw Rectangle
            elif instruction[0] == 'R':
                if len(instruction) == 5:
                    try:
                        p1 = (int(instruction[1]), int(instruction[2]))
                        p2 = (int(instruction[3]), int(instruction[4]))
                        rect_obj = Rectangle((p1, p2), self.cv)
                        rect_obj.draw()
                        self.graph_canvas()
                    except ValueError:
                        print('Invalid line arguments')
                else:
                    print('invalid number of arguments for Draw Rectangle')
                    return
            # Bucket fill
            elif instruction[0] == 'B':
                if len(instruction) == 4:
                    try:
                        point = (int(instruction[1]), int(instruction[2]))
                        color = instruction[3]
                        self.bucket_fill(point, color)
                        self.graph_canvas()
                    except ValueError:
                        print('Invalid line arguments')
                else:
                    print('invalid number of arguments for Bucket Fill')
                    return
            # No valid instruction
            else:
                print(f'invalid instruction {instruction[0]} in input file')
                return

    def graph_canvas(self) -> None:
        width = len(self.cv.canvas[0])
        # heigth = len(canvas)
        h_line = (width + 2) * '-'

        with open('output.txt', 'a') as ofile:
            ofile.write(h_line)
            ofile.write('\n')

            for line in self.cv.canvas:
                line = ''.join(map(str, line))
                # line = str(line).strip('[]')
                line = '|' + line + '|'
                ofile.write(line)
                ofile.write('\n')
            ofile.write(h_line)
            ofile.write('\n')


def read_input_file(file: str) -> tuple:
    """
    Reads the inifile and determine an output
    :param file: ini_file with the canvas and draw description
    :return:
    """
    canvas_instructions = []
    with open(file, encoding='utf8') as f:
        for line in f:
            canvas_instructions.append(line.strip().split())

    canvas_size = canvas_instructions.pop(0)
    return canvas_size, canvas_instructions,


def delete_previous_output() -> None:
    if path.exists("output.txt"):
        os.remove("output.txt")


def main(input_file: str) -> None:
    canvas, instructions = read_input_file(input_file)
    if canvas[0] != 'C' or len(canvas) != 3:
        print('ERROR: Not a valid input file, First command should be a Canvas + size i.e C [X], [Y]')
        return "Not Valid canvas"
    delete_previous_output()
    # TODO: define canvas matrix as ndarray
    dw = Drawer(canvas, instructions)
    dw.graph_canvas()
    dw.graph()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='read information from input.txt and plots to output.txt on a defined '
                                                 'canvas')
    # Optional Arguments
    parser.add_argument('input_file', type=str, default='input.txt', help='provide the location of the input file')
    args = parser.parse_args()
    main(args.input_file)
