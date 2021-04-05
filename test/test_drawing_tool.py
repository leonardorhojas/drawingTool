import pytest
import drawingTool
import figures
from unittest.mock import patch
from Exceptions import BadLineArguments, InvalidCanvas, InvalidArgumentType, InvalidNumberArguments, InvalidPointsRange


def read_file(file):
    file_content = open(file, 'r').read()
    return file_content


def test_main_result():
    """
    Test the test data expected for the following instructions in tesst/files/input.txt:
    C 20 4
    L 1 2 6 2
    L 6 3 6 4
    R 16 1 20 3
    B 10 3 o
    :return:
    """
    # Given
    input_file = 'test/files/input.txt'
    output_generated = "output.txt"
    output_test = 'test/files/output.txt'
    # When
    drawingTool.main(input_file)
    output_expected = read_file(output_test)
    output_returned = read_file(output_generated)
    # Expected
    assert output_returned == output_expected


def test_line_bad_definition():
    # Given
    p1 = (1, 2)
    p2 = (4, 3)
    canvas = object
    # When
    figure = figures.Line((p1, p2), canvas)
    # Expected
    with pytest.raises(BadLineArguments):
        figure.draw()


@patch('drawingTool.read_input_file')
def test_bad_canvas_no_canvas(mock_input_file):
    """
    Test that no canvas where send in the inputfile
    :param mock_input_file:
    :return:
    """
    # Given
    canvas = ['P', 2]
    instructions = ['L', 2, 3]
    # When
    mock_input_file.return_value = canvas, instructions
    # Expected
    with pytest.raises(InvalidCanvas):
        drawingTool.main('input.txt')


def test_bad_instructions():
    """
    Test that an exception raise when a bad Canvas is passed
    :return:
    """
    # Given
    canvas = ['C', 20, 4]
    instructions = ['C', 2, 4, 5, 6]
    # When
    dw = drawingTool.Drawer(canvas, instructions)
    # Expected
    with pytest.raises(InvalidArgumentType):
        dw.graph()


# given
@pytest.mark.parametrize("canvas, instructions", [(['C', 20, 4], [['L', 2, 4, 5, 6, 7]]),
                                                  (['C', 20, 4], [['R', 2, 4, 5, 6, 7]]),
                                                  (['C', 20, 4], [['B', 2, 4, 5, 6, 7]])])
def test_bad_length_instructions(canvas, instructions):
    """
    Test that an exception is raised when worng number of parameters is sent for instructions
    :param canvas: test canvas
    :param instructions: bad set of instructions 5 point instead of 4
    :return:
    """
    # When
    dw = drawingTool.Drawer(canvas, instructions)
    # Expected
    with pytest.raises(InvalidNumberArguments):
        dw.graph()


# given
@pytest.mark.parametrize("canvas, instructions", [(['C', 20, 4], [['L', 2, 4, 'r', 7]]),
                                                  (['C', 20, 4], [['R', 2, 4, 'r', 7]]),
                                                  (['C', 20, 4], [['B', 2, 'b', 'r']])])
def test_bad_data_type_point(canvas, instructions):
    """
    Test that a wrong data type in input.txt trows an excpetion
    :param canvas:test canvas
    :param instructions:bad set of instructions string instead of int
    :return:
    """
    # When
    dw = drawingTool.Drawer(canvas, instructions)
    # Expected
    with pytest.raises(ValueError):
        dw.graph()


# given
@patch('drawingTool.Drawer.validate_point')
@pytest.mark.parametrize("canvas, instructions", [(['C', 20, 4], [['L', 2, 4, 2, 7]]),
                                                  (['C', 20, 4], [['R', 2, 4, 2, 7]]),
                                                  (['C', 20, 4], [['B', 2, 4, 'r']])])
def test_bad_h_v_lines(mock_validate_point,canvas, instructions):
    """
    Test that a wrong data type in input.txt trows an exception
    :param canvas:test canvas
    :param instructions:bad set of instructions string instead of int
    :return:
    """
    # When
    mock_validate_point.return_value = False
    dw = drawingTool.Drawer(canvas, instructions)
    # Expected
    with pytest.raises(InvalidPointsRange):
        dw.graph()
