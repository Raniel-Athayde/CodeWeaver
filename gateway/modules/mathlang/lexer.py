import re
from framework.interfaces import BaseLexer

class MathLangLexer(BaseLexer):
    def tokenize(self, code):
        token_specification = [
            ('NUMBER',   r'\d+(\.\d*)?'),  # Inteiro ou decimal
            ('KEYWORD',  r'PRINT\b'),      # Palavra-chave PRINT
            ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'), # Identificadores (variáveis)
            ('ASSIGN',   r'='),            # Atribuição
            ('OPERATOR', r'[+\-*/]'),      # Operadores aritméticos
            ('LPAREN',   r'\('),           # Abre parênteses
            ('RPAREN',   r'\)'),           # Fecha parênteses
            ('NEWLINE',  r'\n'),           # Nova linha
            ('SKIP',     r'[ \t\r]+'),     # Espaços e tabs
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
            elif kind == 'ID':
                tokens.append({"type": "ID", "value": value})
            elif kind == 'ASSIGN':
                tokens.append({"type": "ASSIGN", "value": value})
            elif kind == 'OPERATOR':
                tokens.append({"type": "OPERATOR", "value": value})
            elif kind == 'LPAREN':
                tokens.append({"type": "LPAREN", "value": value})
            elif kind == 'RPAREN':
                tokens.append({"type": "RPAREN", "value": value})
            elif kind == 'NEWLINE':
                tokens.append({"type": "NEWLINE", "value": value})
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Caractere inesperado: {value}')
        return tokens
