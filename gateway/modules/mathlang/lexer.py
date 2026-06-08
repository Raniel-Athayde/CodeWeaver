import re
from framework.interfaces import BaseLexer

class MathLangLexer(BaseLexer):
    def tokenize(self, code):
        # Regex para capturar KEYWORD, NUMBER, OPERATORS e PARENTHESES
        token_specification = [
            ('NUMBER',   r'\d+(\.\d*)?'),  # Inteiro ou decimal
            ('KEYWORD',  r'PRINT'),        # Palavra-chave PRINT
            ('OPERATOR', r'[+\-*/]'),      # Operadores aritméticos
            ('LPAREN',   r'\('),           # Abre parênteses
            ('RPAREN',   r'\)'),           # Fecha parênteses
            ('SKIP',     r'[ \t]+'),       # Espaços e tabs
            ('MISMATCH', r'.'),             # Qualquer outro caractere
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        tokens = []
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER':
                tokens.append({"type": "NUMBER", "value": value})
            elif kind == 'KEYWORD':
                tokens.append({"type": "KEYWORD", "value": value})
            elif kind == 'OPERATOR':
                tokens.append({"type": "OPERATOR", "value": value})
            elif kind == 'LPAREN':
                tokens.append({"type": "LPAREN", "value": value})
            elif kind == 'RPAREN':
                tokens.append({"type": "RPAREN", "value": value})
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Caractere inesperado: {value}')
        return tokens
