from window import Window, Maze

win = Window(500, 500)
maze = Maze(10, 10, 15, 15, 25, 25, win)

win.wait_for_close()
