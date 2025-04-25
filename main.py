from window import Window, Point, Line

win = Window(800, 600)

point1 = Point(5, 5)
point2 = Point(150, 150)

line = Line(point1, point2)

win.draw_line(line, "red")
win.wait_for_close()
