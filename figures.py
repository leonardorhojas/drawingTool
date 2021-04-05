import abc


class Shape:
    """
    Base class to define geometric figures to plot
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, points: tuple, canvas: object):
        """
        Constructor method for the geometric figures
        :param points: tuple with the point of the geometric figure
        :param canvas: object with the currenct cnavas
        """
        self.p1, self.p2 = points
        self.x1, self.y1 = self.p1
        self.x2, self.y2 = self.p2
        self.canvas = canvas

    @staticmethod
    def range_correction(a: int, b: int):
        """
        adjusts the line order to graph it in the correct path
        :param a: first point
        :param b: second point
        :return: line adjusted with left point first and right pond second
        """
        if a < b:
            line = (a - 1, b)
        else:
            line = (b - 1, a)
        return line

    @abc.abstractmethod
    def draw(self):
        pass


class Line(Shape):
    """
    Class to define an horizontal or vertical line, from p1 to p2
    """

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
    """
    Class to define an Rectangle with left upper point p1, and  right down point p2
    """

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
