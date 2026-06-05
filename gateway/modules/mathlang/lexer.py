class MathLangLexer:
    def tokenize(self, code):
        parts = code.strip().split()
        tokens = []
        for part in parts:
            if part == "PRINT":
                tokens.append({"type": "KEYWORD", "value": "PRINT"})
            elif part in ["+", "-", "*", "/"]:
                tokens.append({"type": "OPERATOR", "value": part})
            elif part.replace('.', '', 1).isdigit():
                tokens.append({"type": "NUMBER", "value": part})
        return tokens
