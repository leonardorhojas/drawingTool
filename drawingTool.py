import argparse
import os.path
from os import path
from typing import Optional

from Exceptions import InvalidPointsRange, InvalidNumberArguments, InvalidArgumentType
from figures import Line, Rectangle
import numpy as np


class Canvas:
    """
    Class to define the Canvas used to plot the graphics, it creates an nested list or a an ndarray
    """

    def __init__(self, canvas):
        self.canvas_size = canvas
        self.canvas = np.full((int(self.canvas_size[2]), int(self.canvas_size[1])), ' ')


class Drawer:

    def __init__(self, canvas: list, instructions: list):
        self.cv = Canvas(canvas)
        self.instructions = instructions

    def bucket_fill(self, start_coords: tuple, fill_value: str) -> None:
        """
        Bucket fill algorithm
        data : (Y, X) ndarray of uint8 type
            Image with flood to be filled. Modified inplace.
        start_coords : tuple
            Length-2 tuple of ints defining (row/y, col/x) start coordinates.
        fill_value : int
            Value the flooded area will take after the fill.

        Returns
        -------
        None, ``data`` is modified inplace.
        """
        xsize, ysize = self.cv.canvas.shape
        orig_value = self.cv.canvas[start_coords[0], start_coords[1]]

        stack = set(((start_coords[0], start_coords[1]),))
        if fill_value == orig_value:
            raise ValueError("Filling region with same value "
                             "already present is unsupported. "
                             "Did you already fill this region?")

        while stack:
            x, y = stack.pop()
            if self.cv.canvas[x, y] == orig_value:
                self.cv.canvas[x, y] = fill_value
                if x > 0:
                    stack.add((x - 1, y))
                if x < (xsize - 1):
                    stack.add((x + 1, y))
                if y > 0:
                    stack.add((x, y - 1))
                if y < (ysize - 1):
                    stack.add((x, y + 1))

    def graph(self) -> Optional[None]:
        """
        Factory method to create an geometrical object according to the parameter set in the ini_file
        :return:
        """
        # for step in list_steps:
        for instruction in self.instructions:
            # Draw Line
            try:
                if instruction[0] == 'L':
                    try:
                        if len(instruction) == 5:
                            try:
                                p1 = int(instruction[1]), int(instruction[2])
                                p2 = int(instruction[3]), int(instruction[4])
                            except ValueError:
                                print('Invalid line arguments')
                            try:
                                if self.validate_point(p1) and self.validate_point(p2):
                                    line_obj = Line((p1, p2), self.cv)
                                    line_obj.draw()
                                    self.graph_canvas()
                                else:
                                    raise InvalidPointsRange
                            except InvalidPointsRange:
                                print(f'Invalid range for line, line should be between x 1:{self.cv.canvas_size[1]} '
                                      f'and 1:{self.cv.canvas_size[2]}')
                        else:
                            raise InvalidNumberArguments
                    except InvalidNumberArguments:
                        print('invalid number of arguments for Draw line')
                # Draw Rectangle
                elif instruction[0] == 'R':
                    try:
                        if len(instruction) == 5:
                            try:
                                p1 = (int(instruction[1]), int(instruction[2]))
                                p2 = (int(instruction[3]), int(instruction[4]))
                            except ValueError:
                                print('Invalid line arguments')
                            try:
                                if self.validate_point(p1) and self.validate_point(p2):
                                    rect_obj = Rectangle((p1, p2), self.cv)
                                    rect_obj.draw()
                                    self.graph_canvas()
                                else:
                                    raise InvalidPointsRange
                            except InvalidPointsRange:
                                print(f'Invalid range for rectangle, rectangle should be between '
                                      f'x 1:{self.cv.canvas_size[1]} and 1:{self.cv.canvas_size[2]}')
                        else:
                            raise InvalidNumberArguments
                    except InvalidNumberArguments:
                        print('invalid number of arguments for Draw Rectangle')

                # Bucket fill
                elif instruction[0] == 'B':
                    try:
                        if len(instruction) == 4:
                            try:
                                point = (int(instruction[1]), int(instruction[2]))
                                color = instruction[3]
                            except ValueError:
                                print('Invalid line arguments')
                            try:
                                if self.validate_point(point):
                                    point = (int(instruction[2]), int(instruction[1]),)
                                    self.bucket_fill(point, color)
                                    self.graph_canvas()
                                else:
                                    raise InvalidPointsRange
                            except InvalidPointsRange:
                                print(f'Invalid point for bucket fill, should be between '
                                      f'x 1:{self.cv.canvas_size[1]} and 1:{self.cv.canvas_size[2]}')
                        else:
                            raise InvalidNumberArguments
                    except InvalidNumberArguments:
                        print('invalid number of arguments for Bucket Fill')

                # No valid instruction
                else:
                    raise InvalidArgumentType
            except InvalidArgumentType:
                print(f'invalid instruction {instruction[0]} in input file')
                return

    def graph_canvas(self) -> None:
        canvas = self.cv.canvas.tolist()
        width = len(canvas[0])
        # heigth = len(canvas)
        h_line = (width + 2) * '-'

        with open('output.txt', 'a') as ofile:
            ofile.write(h_line)
            ofile.write('\n')

            for line in canvas:
                line = ''.join(map(str, line))
                line = '|' + line + '|'
                ofile.write(line)
                ofile.write('\n')
            ofile.write(h_line)
            ofile.write('\n')

    def validate_point(self, point):
        x, y = point
        if 1 <= x <= int(self.cv.canvas_size[1]) and 1 <= y <= int(self.cv.canvas_size[2]):
            return True
        else:
            return False


def read_input_file(file: str) -> tuple:
    """
    Reads parameters from the ini_file
    :param file: ini_file with the canvas and draw description
    :return: tuple (canvas_size, canvas_instructions) for plot accordingly
    """
    canvas_instructions = []
    with open(file, encoding='utf8') as f:
        for line in f:
            canvas_instructions.append(line.strip().split())

    canvas_size = canvas_instructions.pop(0)
    return canvas_size, canvas_instructions,


def delete_previous_output() -> None:
    """
    Deletes existing output.txt if applies
    :return: None
    """
    if path.exists("output.txt"):
        os.remove("output.txt")


def main(input_file: str) -> None:
    canvas, instructions = read_input_file(input_file)
    if canvas[0] != 'C' or len(canvas) != 3 or int(canvas[1]) < 1 or int(canvas[2]) < 1:
        print('ERROR: Not a valid input.txt, First command should be a Canvas, '
              'size i.e C [X], [Y] X and Y must be > 0')
        return "Not Valid canvas"
    delete_previous_output()
    dw = Drawer(canvas, instructions)
    dw.graph_canvas()
    dw.graph()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='read information from input.txt and plots to output.txt '
                                                 'on a defined canvas')
    # Optional Arguments
    parser.add_argument('--input_file', type=str, default='input.txt', help='provide the location of the input file')
    args = parser.parse_args()
    main(args.input_file)
