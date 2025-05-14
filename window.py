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
    def __init__(self, window=None, x1=None, x2=None, y1=None, y2=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
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
        self.seed = seed
        self._create_cells()

    # TODO implement seed properly, using random.seed()
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

        if self.seed is None:
            self._break_walls_r(
                random.randrange(self.num_rows), random.randrange(self.num_cols)
            )
        else:
            self._break_walls_r(self.seed[0], self.seed[1])

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

    def _break_walls_r(self, row, col):
        self._cells[col][row].visited = True

        while True:
            neighbors = self._check_neighbors(row, col)

            if len(neighbors) == 0:
                self._cells[col][row].draw()
                return

            move_to = random.randrange(len(neighbors))

            self._break_wall(
                neighbors[move_to][0], neighbors[move_to][1], neighbors[move_to][2]
            )
            self._break_walls_r(neighbors[move_to][0], neighbors[move_to][1])

    def _reset_cells_visited(self):
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                if self._cells[col][row].visited:
                    self._cells[col][row].visited = False

    def _check_neighbors(self, row, col):
        neighbors = []

        if row > 0 and not self._cells[col][row - 1].visited:
            neighbors.append((row - 1, col, "left"))
        if row < self.num_rows - 1 and not self._cells[col][row + 1].visited:
            neighbors.append((row + 1, col, "right"))
        if col > 0 and not self._cells[col - 1][row].visited:
            neighbors.append((row, col - 1, "up"))
        if col < self.num_cols - 1 and not self._cells[col + 1][row].visited:
            neighbors.append((row, col + 1, "down"))

        return neighbors

    def _break_wall(self, row, col, direction):
        if direction == "left":
            self._cells[col][row].has_right_wall = False
            self._cells[col][row + 1].has_left_wall = False
            self._draw_cell(row + 1, col)

        if direction == "right":
            self._cells[col][row].has_left_wall = False
            self._cells[col][row - 1].has_right_wall = False
            self._draw_cell(row - 1, col)
        if direction == "up":
            self._cells[col][row].has_bottom_wall = False
            self._cells[col + 1][row].has_top_wall = False
            self._draw_cell(row, col + 1)

        if direction == "down":
            self._cells[col][row].has_top_wall = False
            self._cells[col - 1][row].has_bottom_wall = False
            self._draw_cell(row, col - 1)

        self._draw_cell(row, col)

    def _animate(self):
        if self._win:
            self._win.redraw()
            time.sleep(0.005)

    def solve(self):
        self._solve_r(0, 0)

    def _solve_r(self, row, col):
        self._animate()
        self._cells[col][row].visited = True

        if self._cells[col][row] == self._cells[-1][-1]:
            return True

        if (
            row > 0
            and not self._cells[col][row - 1].visited
            and not self._cells[col][row].has_left_wall
        ):
            self._cells[col][row].draw_move(self._cells[col][row - 1])
            if self._solve_r(row - 1, col):
                return True
            self._cells[col][row].draw_move(self._cells[col][row - 1], True)

        if (
            row < self.num_rows - 1
            and not self._cells[col][row + 1].visited
            and not self._cells[col][row].has_right_wall
        ):
            self._cells[col][row].draw_move(self._cells[col][row + 1])
            if self._solve_r(row + 1, col):
                return True
            self._cells[col][row].draw_move(self._cells[col][row + 1], True)

        if (
            col > 0
            and not self._cells[col - 1][row].visited
            and not self._cells[col][row].has_top_wall
        ):
            self._cells[col][row].draw_move(self._cells[col - 1][row])
            if self._solve_r(row, col - 1):
                return True
            self._cells[col][row].draw_move(self._cells[col - 1][row], True)

        if (
            col < self.num_cols - 1
            and not self._cells[col + 1][row].visited
            and not self._cells[col][row].has_bottom_wall
        ):
            self._cells[col][row].draw_move(self._cells[col + 1][row])
            if self._solve_r(row, col + 1):
                return True
            self._cells[col][row].draw_move(self._cells[col + 1][row], True)

        return False
