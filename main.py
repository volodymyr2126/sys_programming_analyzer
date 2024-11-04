from analysis.lexer import Lexer
from analysis.parser import Parser

test_input = [
    "побудувати точку ((1+2*(1)),1)",
    "провести пряму за двома точками (1,2) (3,4)",
    "побудувати перпендикуляр до прямої за двома точками (1,2) (3,4) з точки (5,10)",
    "побудувати трикутник за трьома точками (0,0) (3,0) (1.5,10)",
    "побудувати квадрат з точки (1,5) з стороною (2+3)"
]


def test_geometry(input_texts):
    for text in input_texts:
        print(f"Testing input: {text}")
        parser = Parser(text)
        try:
            parser.parse()
            tree = parser.execution_tree
            tree.build()
        except Lexer.LexicalError as e:
            print(e)


if __name__ == '__main__':
    test_geometry(test_input)
