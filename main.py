from window import Window, Maze

win = Window(500, 500)
maze = Maze(10, 10, 15, 15, 25, 25, win)
maze._reset_cells_visited()
maze.solve()
win.wait_for_close()
