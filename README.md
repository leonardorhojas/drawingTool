# Drawing Tool

In a nutshell, the program reads the `input.txt`, executes a set of commands from the file, step by step, and produces 
`output.txt`

you optionally can pass an input file in a remote folder with the option:

```
python drawinTool.py input_file "/other/foler/input.txt"
```

Otherwise it will use the input.txt expected inside the project folder

## Usage

```
python drawinTool.py
```

At this time, the functionality of the program is quite limited but this might change in the future.
At the moment, the program should support the following set of commands:

`C w h` _Create Canvas_: Should create a new canvas of width w and height h.

`L x1 y1 x2 y2` _Create Line_: Should create a new line from (x1,y1) to (x2,y2). Currently
only horizontal or vertical lines are supported. Horizontal and vertical
lines will be drawn using the `'x' `character.

`R x1 y1 x2 y2 ` _Create Rectangle_: Should create a new rectangle, whose upper left
corner is (x1,y1) and lower right corner is `(x2,y2)`. Horizontal and vertical
lines will be drawn using the 'x' character.

`B x y c` _Bucket Fill_: Should fill the entire area connected to (x,y) with "colour" c.
The behaviour of this is the same as that of the "bucket fill" tool in paint
programs

You can only draw if a canvas has been created.

You can only draw objects within the size of the canvas

## Installation

```cd drawingTool

pip install -r requirements.txt
```

## License
[MIT](https://choosealicense.com/licenses/mit/)