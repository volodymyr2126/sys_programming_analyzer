import re
from matplotlib import pyplot as plt

from analysis.lexer import Lexer
from utils.shapes import Point, Line, Triangle, Perpendicular, Square


class Node:
    def __init__(self, value):
        self.value = value


class ShapeNode(Node):
    def __init__(self, value: str):
        super().__init__(value)


class PointNode(ShapeNode):
    def __init__(self, value: str, x_node: Node, y_node: Node):
        super().__init__(value)
        self.x = x_node
        self.y = y_node
        self.shape_built = False
        self.shape = None

    def build_shape(self):
        self.shape = Point(self.x.value, self.y.value)
        self.shape_built = True


class LineNode(ShapeNode):
    def __init__(self, value: str, a_node: PointNode, b_node: PointNode):
        super().__init__(value)
        self.a = a_node
        self.b = b_node
        self.shape_built = False
        self.shape = None

    def build_shape(self):
        self.a.build_shape()
        self.b.build_shape()
        self.shape = Line(self.a.shape, self.b.shape)
        self.shape_built = True


class PerpendicularNode(ShapeNode):
    def __init__(self, value: str, line: LineNode, a_node: PointNode):
        super().__init__(value)
        self.line = line
        self.a = a_node
        self.shape = None
        self.shape_built = False

    def build_shape(self):
        self.line.build_shape()
        self.a.build_shape()
        self.shape = Perpendicular(self.line.shape, self.a.shape)
        self.shape_built = True


class TriangleNode(ShapeNode):
    def __init__(self, value: str, a_node: PointNode, b_node: PointNode, c_node: PointNode):
        super().__init__(value)
        self.a = a_node
        self.b = b_node
        self.c = c_node
        self.shape_built = False
        self.shape = None

    def build_shape(self):
        self.a.build_shape()
        self.b.build_shape()
        self.c.build_shape()
        self.shape = Triangle(self.a.shape, self.b.shape, self.c.shape)
        self.shape_built = True


class SquareNode(ShapeNode):
    def __init__(self, value: str, left: PointNode, length: Node):
        super().__init__(value)
        self.start_point = left
        self.length = length
        self.shape = None
        self.shape_built = False

    def build_shape(self):
        self.start_point.build_shape()
        self.shape = Square(self.start_point.shape, self.length.value)
        self.shape_built = True


class BuildNode:
    def __init__(self, build_word, shape: ShapeNode):
        self.build_word = build_word
        self.child = shape


class ExecutionTree:
    def __init__(self):
        self.start_node = None

    def start(self, start_node: BuildNode):
        self.start_node = start_node

    def build(self):
        if not self.start_node:
            raise ValueError("Дерево виконання порожнє. Немає жодної фігури для побудови.")

        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.grid(True)

        self._draw_node(ax)

        plt.show()

    def _draw_node(self, ax):
        self.start_node.child.build_shape()
        self.start_node.child.shape.draw(ax)


class Parser:
    def __init__(self, input_text: str):
        self.input_text = input_text
        self.lexer = Lexer(self.input_text)
        self.execution_tree = ExecutionTree()
        self.current_index = 0

    def parse(self):
        lexeme_list = self.lexer.analyze()
        while self.current_index < len(lexeme_list):
            lexeme, token_type = lexeme_list[self.current_index]
            if token_type == "FUNC":
                self.current_index += 1
                shape_node = self.parse_shape(lexeme_list)
                if shape_node:
                    build_node = BuildNode(lexeme, shape_node)
                    self.execution_tree.start(build_node)

            self.current_index += 1

    def parse_shape(self, lexeme_list):
        lexeme, token_type = lexeme_list[self.current_index]

        if token_type == "SHAPE":
            if re.match("точ", lexeme, re.IGNORECASE):
                return self.parse_point(lexeme_list)
            elif re.match("прям", lexeme, re.IGNORECASE):
                return self.parse_line(lexeme_list)
            elif re.match("перпендик", lexeme, re.IGNORECASE):
                return self.parse_perpendicular(lexeme_list)
            elif re.match("трикутн", lexeme, re.IGNORECASE):
                return self.parse_triangle(lexeme_list)
            elif re.match("квадрат", lexeme, re.IGNORECASE):
                return self.parse_square(lexeme_list)
        return None

    def parse_point(self, lexeme_list):
        self.current_index += 1
        try:
            x, y = (eval(lexeme_list[self.current_index][0].split(",")[0][1:]),
                eval(lexeme_list[self.current_index][0].split(",")[1][:-1]))
            x_node = Node(float(x))
            y_node = Node(float(y))
            return PointNode("точка",x_node, y_node)
        except Exception as e:
            raise SyntaxError("Неправильний формат для точки.")

    def parse_line(self, lexeme_list):
        self.current_index += 1
        while lexeme_list[self.current_index][1] != "QUANTITY":
            self.current_index += 1
        if not re.match("дв", lexeme_list[self.current_index][0], re.IGNORECASE):
            raise SyntaxError("Пряма будується за двома точками")
        self.current_index += 1
        if re.match('точк', lexeme_list[self.current_index][0], re.IGNORECASE):
            a_node = self.parse_point(lexeme_list)
            b_node = self.parse_point(lexeme_list)
            line_node = LineNode("прям", a_node, b_node)
            return line_node

    def parse_perpendicular(self, lexeme_list):
        self.current_index += 1
        line_node = self.parse_line(lexeme_list)
        while lexeme_list[self.current_index][1] != "SHAPE":
            self.current_index += 1
        a_node = self.parse_point(lexeme_list)
        perpendicular_node = PerpendicularNode("перпендик", line_node, a_node)
        return perpendicular_node

    def parse_triangle(self, lexeme_list):
        self.current_index += 1
        while lexeme_list[self.current_index][1] != "QUANTITY":
            self.current_index += 1
        if not re.match("тр", lexeme_list[self.current_index][0], re.IGNORECASE):
            raise SyntaxError("Трикутник будується за трьома точками")
        self.current_index += 1
        if re.match('точк', lexeme_list[self.current_index][0], re.IGNORECASE):
            a_node = self.parse_point(lexeme_list)
            b_node = self.parse_point(lexeme_list)
            c_node = self.parse_point(lexeme_list)
            triangle_node = TriangleNode("трикутник", a_node, b_node, c_node)
            return triangle_node

    def parse_square(self, lexeme_list):
        self.current_index += 1
        while lexeme_list[self.current_index][1] != "SHAPE":
            self.current_index += 1
        bottom_left_node = self.parse_point(lexeme_list)
        while lexeme_list[self.current_index][1] != "SHAPE":
            self.current_index += 1
        self.current_index += 1
        length_lexeme, length_type = lexeme_list[self.current_index]
        if length_type == "NUMBER" or length_type == "POINT":
            length_node = Node(float(eval(length_lexeme)))
            square_node = SquareNode("квадрат", bottom_left_node, length_node)
            self.current_index += 1
            return square_node
        raise SyntaxError("Очікувалася довжина сторони квадрату")
