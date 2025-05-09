import time
from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__running = False
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, width=width, height=height, bg="white")
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, canvas, fill_color):

        canvas.create_line(
            self.start.x, self.start.y, self.end.x, self.end.y, fill=fill_color, width=2
        )


class Cell:
    def __init__(self, window=None, x1=0, x2=0, y1=0, y2=0):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = window

    def draw(self, x1, x2, y1, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        # TODO redesign this section
        if self._win:

            if self.has_left_wall:
                self._win.draw_line(
                    Line(Point(self._x1, self._y1), Point(self._x1, self._y2)),
                    "black",
                )
            else:
                self._win.draw_line(
                    Line(Point(self._x1, self._y1), Point(self._x1, self._y2)),
                    "white",
                )
            if self.has_right_wall:
                self._win.draw_line(
                    Line(Point(self._x2, self._y1), Point(self._x2, self._y2)),
                    "black",
                )
            else:
                self._win.draw_line(
                    Line(Point(self._x2, self._y1), Point(self._x2, self._y2)),
                    "white",
                )
            if self.has_top_wall:
                self._win.draw_line(
                    Line(Point(self._x1, self._y1), Point(self._x2, self._y1)),
                    "black",
                )
            else:
                self._win.draw_line(
                    Line(Point(self._x1, self._y1), Point(self._x2, self._y1)),
                    "white",
                )
            if self.has_bottom_wall:
                self._win.draw_line(
                    Line(Point(self._x1, self._y2), Point(self._x2, self._y2)),
                    "black",
                )
            else:
                self._win.draw_line(
                    Line(Point(self._x1, self._y2), Point(self._x2, self._y2)),
                    "white",
                )

    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "grey"

        self._win.draw_line(
            Line(
                Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2),
                Point((to_cell._x1 + to_cell._x2) / 2, (to_cell._y1 + to_cell._y2) / 2),
            ),
            color,
        )


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()

    def _create_cells(self):
        for col in range(self.num_cols):
            r = []
            for row in range(self.num_rows):
                r.append(Cell(self._win))
            self._cells.append(r)

        for col in range(self.num_cols):
            for row in range(self.num_rows):
                self._draw_cell(row, col)

        self._break_entrance_and_exit()

    def _draw_cell(self, row, col):
        x1 = self.x1 + (row * self.cell_size_x)
        x2 = x1 + self.cell_size_x
        y1 = self.y1 + (col * self.cell_size_y)
        y2 = y1 + self.cell_size_y

        self._cells[col][row].draw(x1, x2, y1, y2)
        self._animate()

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)

        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(
            self.num_rows - 1,
            self.num_cols - 1,
        )

    def _animate(self):
        if self._win:
            self._win.redraw()
            time.sleep(0.03)
