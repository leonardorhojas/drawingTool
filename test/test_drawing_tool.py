import pytest
import os.path
from os import path
import drawingTool
# import mock


def read_file(file):
    str = open(file, 'r').read()
    return str


def test_result():
    # from drawingTool import main
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


def test_main_parse():
    pass