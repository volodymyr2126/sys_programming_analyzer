import re


class Lexer:
    class LexicalError(Exception):
        def __init__(self, token):
            super().__init__(f"Помилка під час парсингу в наступному слові: {token}")

    def __init__(self, input_text: str):
        self.input_text = input_text
        self.token_specs = {
            "NUMBER": r'^[-+]?\d+(\.\d+)?$',
            'IDENTIFIER': r'^([A-Za-z]+[A-Za-z]*)$',
            'FUNC': r'^(побуду|прове)',
            'RESERVED': r'^(за|через|до|в|з)$',
            'SHAPE': r'^(точ|трикутник|прям|вершин|квадрат|перпендик|сторон)',
            'QUANTITY': r'^(дв|тр)',
            'POINT': r'\(.*\)'
        }
        self.delimiters = [" ", "\t", "\n",]

    def identify(self, lexeme):
        for token_type, pattern in self.token_specs.items():
            if re.match(pattern, lexeme, re.IGNORECASE):
                return lexeme, token_type
        raise self.LexicalError(lexeme)

    def analyze(self):
        line = 1
        pos = 0
        identified_lexemes = []
        lexeme = ""
        for ch in self.input_text:
            pos += 1
            if ch in self.delimiters:
                if len(lexeme) > 0:
                    identified = self.identify(lexeme)
                    identified_lexemes.append(identified)
                    lexeme = ""
                if ch == "\n":
                    line += 1
                    pos = 0
                continue
            else:
                lexeme += ch
        pos += 1
        if len(lexeme) > 0:
            identified = self.identify(lexeme)
            identified_lexemes.append(identified)

        return identified_lexemes
