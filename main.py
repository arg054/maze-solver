from window import Window, Cell, Maze

win = Window(800, 600)
maze = Maze(10, 10, 10, 10, 50, 50, win)

win.wait_for_close()
