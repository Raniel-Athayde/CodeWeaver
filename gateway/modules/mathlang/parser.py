from framework.interfaces import BaseParser

class MathLangParser(BaseParser):
    def parse(self, tokens):
        self.tokens = tokens
        self.pos = 0
        
        ast = {"type": "PrintStatement", "children": [], "metadata": {}}
        
        if self.current_token() and self.current_token()["type"] == "KEYWORD" and self.current_token()["value"] == "PRINT":
            self.advance()
            expression = self.parse_expression()
            if expression:
                ast["children"].append(expression)
        
        return ast

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        self.pos += 1

    def parse_expression(self):
        # Expressão = Termo (('+' | '-') Termo)*
        node = self.parse_term()
        
        while self.current_token() and self.current_token()["type"] == "OPERATOR" and self.current_token()["value"] in ("+", "-"):
            operator = self.current_token()["value"]
            self.advance()
            right = self.parse_term()
            node = {
                "type": "BinaryExpression",
                "metadata": {"operator": operator},
                "children": [node, right]
            }
        return node

    def parse_term(self):
        # Termo = Fator (('*' | '/') Fator)*
        node = self.parse_factor()
        
        while self.current_token() and self.current_token()["type"] == "OPERATOR" and self.current_token()["value"] in ("*", "/"):
            operator = self.current_token()["value"]
            self.advance()
            right = self.parse_factor()
            node = {
                "type": "BinaryExpression",
                "metadata": {"operator": operator},
                "children": [node, right]
            }
        return node

    def parse_factor(self):
        # Fator = NUMBER | '(' Expressão ')'
        token = self.current_token()
        if not token:
            return None
            
        if token["type"] == "NUMBER":
            self.advance()
            return {"type": "LiteralNumber", "metadata": {"value": token["value"]}}
        
        if token["type"] == "LPAREN":
            self.advance()
            node = self.parse_expression()
            if self.current_token() and self.current_token()["type"] == "RPAREN":
                self.advance()
                return node
            else:
                raise RuntimeError("Esperado ')'")
                
        raise RuntimeError(f"Token inesperado: {token['value']}")
