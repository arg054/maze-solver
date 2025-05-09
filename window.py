import random
import time
from tkinter import Tk, BOTH, Canvas


# TODO split window file into class files
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
    def __init__(self, window=None, x1=None, x2=None, y1=None, y2=None, visited=False):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = visited
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = window

    def draw(self, x1=None, x2=None, y1=None, y2=None):
        # TODO redesign this section
        if x1:
            self._x1 = x1
        if x2:
            self._x2 = x2
        if y1:
            self._y1 = y1
        if y2:
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
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()
        self.seed = seed

        if self.seed:
            self.seed = random.seed(seed)

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

    def _get_directions(self, row, col):
        neighbors = []

        # TODO redesign as a switch case?
        if self._col(row - 1, col):
            neighbors.append((row - 1, col))
        else:
            neighbors.append(None)
        if self._col(row + 1, col):
            neighbors.append((row + 1, col))
        else:
            neighbors.append(None)
        if self._col(row, col - 1):
            neighbors.append((row, col - 1))
        else:
            neighbors.append(None)
        if self._col(row, col + 1):
            neighbors.append((row, col + 1))
        else:
            neighbors.append(None)

        return neighbors

    def _break_walls_r(self, row, col):
        self._cells[col][row].visited = True

        while True:
            neighbors = self._get_directions(row, col)

            if not neighbors:
                self._cells[col][row].draw()
                return

            move_to = random(3)
            if move_to:
                # TODO break wall on current cell and on chosen neighbor cell
                self._break_walls_r(move_to[0], move_to[1])

    def _animate(self):
        if self._win:
            self._win.redraw()
            time.sleep(0.03)


"""
            loop though adjacent col,row pairs
                if exists
                    if not visited
                        add to neighbors

            if not neighbors
                draw self._cells[col][row].draw()
                return
            move_to = random(3)
            if move_to:
                self._break_walls_r(move_to[0], move_to[1])

----------------
def get_directions(self, row, col)
    neighbors = []

    if left_neighbor(row-1,col):
        neighbors.append((row-1,col))
    else:
        neighbors.append(None)
    if right_neighbor(row+1,col)
        neighbors.append((row+1,col))
    else:
        neighbors.append(None)
    if above_neighbor(row,col-1)
        neighbors.append((row,col-1))
    else:
        neighbors.append(None)
    if below_neighbor(row,col+1)
        neighbors.append((row,col+1))
    else:
        neighbors.append(None)

    return neighbors
            
----------------
logic for random
0-left
1-right
2-up
3-down       
----------------
neighbor logic
00	01	02	03	04
10	11	12	13	14
20	21	22	23	24

left_neighbor(row-1,col)
right_neighbor(row+1,col)
above_neighbor(row,col-1)
below_neighbor(row,col+1)
----------------
def _break_walls(self, current_cell, wall_to_break):
    if wall_to_break == 0:
        self._cells[current_cell(1)][current_cell(0)].has_left_wall = False
        self._cells[current_cell(1)][current_cell(0)-1].has_right_wall = False
    if wall_to_break == 1:
        self._cells[current_cell(1)][current_cell(0)].has_right_wall = False
        self._cells[current_cell(1)][current_cell(0)+1].has_left_wall = False
    if wall_to_break == 2:
        self._cells[current_cell(1)][current_cell(0)].has_right_wall = False
        self._cells[current_cell(1)][current_cell(0)+1].has_left_wall = False
    if wall_to_break == 3:
        self._cells[current_cell(1)][current_cell(0)].has_right_wall = False
        self._cells[current_cell(1)][current_cell(0)+1].has_left_wall = False
"""
