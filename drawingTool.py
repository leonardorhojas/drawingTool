import argparse
import os.path
from os import path
import numpy as np


class DrawingCanvas:

    def __init__(self, canvas, instructions):
        self.canvas_det = canvas
        self.canvas = [[' ' for x in range(int(self.canvas_det[1]))] for y in range(int(self.canvas_det[2]))]
        self.instructions = instructions

    def draw_line(self, x1, y1, x2, y2, show_canvas=True):
        # TODO: Check for just horizontal and vertical lines
        # draw vertical line
        if x1 == x2:
            x = int(x1) - 1
            for i in range(int(y1) - 1, int(y2)):
                self.canvas[i][x] = 'x'
        # draw horizontal line
        elif y2 == y2:

            y = int(y1) - 1
            for i in range(int(x1) - 1, int(x2)):
                self.canvas[y][i] = 'x'
        else:
            print('Not valid coordinates to plot a line h/v')

        if show_canvas:
            self.draw_canvas()

    def draw_rectangle(self, x1, y1, x2, y2):
        # TODO: Validate range of canvas
        # calc implicit points
        x1_p = x2
        y1_p = y1
        x2_p = x1
        y2_p = y2
        # draw_horizontal_lines
        self.draw_line(x1, y1, x1_p, y1_p, False)
        self.draw_line(x2_p, y2_p, x2, y2, False)

        # draw_vertical_lines
        self.draw_line(x1, y1, x2_p, y2_p, False)
        self.draw_line(x1_p, y1_p, x2, y2, False)

        self.draw_canvas()

    def bucket_fill(self, start_coords, fill_value):
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
        xsize = len(self.canvas[0])
        ysize = len(self.canvas)
        orig_value = self.canvas[start_coords[1]][start_coords[0]]

        stack = set(((start_coords[0], start_coords[1]),))
        if fill_value == orig_value:
            raise ValueError("Filling region with same value "
                             "already present is unsupported. "
                             "Did you already fill this region?")

        while stack:
            x, y = stack.pop()

            if self.canvas[y][x] == orig_value:
                self.canvas[y][x] = fill_value
                if x > 0:
                    stack.add((x - 1, y))
                if x < (xsize - 1):
                    stack.add((x + 1, y))
                if y > 0:
                    stack.add((x, y - 1))
                if y < (ysize - 1):
                    stack.add((x, y + 1))
        self.draw_canvas()

    def draw(self):
        # for step in list_steps:
        for instruction in self.instructions:
            if instruction[0] == 'L':
                # TODO: pass ordered the line coordinates
                self.draw_line(int(instruction[1]), int(instruction[2]), int(instruction[3]), int(instruction[4]), True)
            if instruction[0] == 'R':
                self.draw_rectangle(int(instruction[1]), int(instruction[2]), int(instruction[3]), int(instruction[4]))
            if instruction[0] == 'B':
                self.bucket_fill((int(instruction[1]), int(instruction[2])), instruction[3])

    def draw_canvas(self):
        width = len(self.canvas[0])
        # heigth = len(canvas)
        h_line = (width + 2) * '-'

        with open('output.txt', 'a') as ofile:
            ofile.write(h_line)
            ofile.write('\n')

            for line in self.canvas:
                line = ''.join(map(str, line))
                # line = str(line).strip('[]')
                line = '|' + line + '|'
                ofile.write(line)
                ofile.write('\n')
            ofile.write(h_line)
            ofile.write('\n')


def read_input_file(file) -> list:
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


def delete_previous_output():
    if path.exists("output.txt"):
        os.remove("output.txt")


def main(input_file):
    canvas, instructions = read_input_file(input_file)
    # TODO:  include checking valid instructions per line
    delete_previous_output()
    # TODO: define canvas matrix as ndarray
    dw = DrawingCanvas(canvas, instructions)
    dw.draw_canvas()
    dw.draw()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='read information from input.txt and plots to output.txt on a defined '
                                                 'canvas')
    # Optional Arguments
    parser.add_argument('input_file', type=str, default='input.txt', help='provide the location of the input file')
    args = parser.parse_args()
    main(args.input_file)

