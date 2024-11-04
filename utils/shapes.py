class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def draw(self, ax, color='black'):
        ax.plot(self.x, self.y, 'o', color=color)


class Line:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b
        self.m = (b.y - a.y) / (b.x - a.x) if b.x != a.x else None
        self.k = a.y - self.m * a.x if self.m is not None else None
        self.equation = f"y = {self.m}x + {self.b}" if self.m is not None else f"x = {self.a.x}"

    def draw(self, ax, color='blue'):
        if self.m is not None:
            x_vals = [self.a.x - 10, self.b.x + 10]
            y_vals = [self.m * x + self.k for x in x_vals]
            ax.plot(x_vals, y_vals, color=color)
        else:
            y_vals = [self.a.y - 10, self.a.y + 10]
            ax.plot([self.a.x, self.a.x], y_vals, color=color)


class Perpendicular:
    def __init__(self, l: Line, a: Point):
        self.point = a
        self.line = l
        self.m = -1 / l.m if l.m is not None else None
        self.k = a.y - self.m * a.x if self.m is not None else None
        if self.m is not None:
            x_collision = (self.k - l.k) / (l.m - self.m)
            y_collision = l.m * x_collision + l.k
            self.point_of_collision = Point(x_collision, y_collision)
        else:
            self.point_of_collision = None
        self.equation = f"y = {self.m}x + {self.k}" if self.m is not None else f"x = {a.x}"

    def draw(self, ax, color='green'):
        if self.point_of_collision:
            self.line.draw(ax, color)

            ax.plot(self.point.x, self.point.y, 'o', color=color)

            ax.plot([self.point.x, self.point_of_collision.x],
                    [self.point.y, self.point_of_collision.y],
                    color=color, linestyle='--')

class Triangle:
    def __init__(self, a: Point, b: Point, c: Point):
        self.a = a
        self.b = b
        self.c = c

    def draw(self, ax, color='red'):
        ax.plot([self.a.x, self.b.x, self.c.x, self.a.x],
                [self.a.y, self.b.y, self.c.y, self.a.y], color=color)


class Square:
    def __init__(self, bottom_left: Point, length: float):
        self.bottom_left = bottom_left
        self.length = length

    def draw(self, ax, color='purple'):
        x, y = self.bottom_left.x, self.bottom_left.y
        ax.plot([x, x + self.length, x + self.length, x, x],
                [y, y, y + self.length, y + self.length, y], color=color)
