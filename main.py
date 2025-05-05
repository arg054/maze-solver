from window import Window, Cell

win = Window(800, 600)

cell1 = Cell(5, 50, 5, 50, win)
cell2 = Cell(50, 100, 50, 100, win)

cell1.has_left_wall = False
cell2.has_right_wall = False

cell1.draw("black")
cell2.draw("black")
win.wait_for_close()
