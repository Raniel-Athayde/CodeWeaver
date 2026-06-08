from framework.interfaces import BaseParser

class MathLangParser(BaseParser):
    def parse(self, tokens):
        self.tokens = tokens
        self.pos = 0
        program_ast = {"type": "Program", "body": [], "metadata": {}}
        
        while self.current_token():
            if self.current_token()["type"] == "NEWLINE":
                self.advance()
                continue
            statement = self.parse_statement()
            if statement:
                program_ast["body"].append(statement)
            else:
                break
        return program_ast

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        self.pos += 1

    def parse_statement(self):
        token = self.current_token()
        if not token: return None

        # PRINT <expr>
        if token["type"] == "KEYWORD" and token["value"] == "PRINT":
            self.advance()
            expression = self.parse_expression()
            self.consume_newline()
            return {"type": "PrintStatement", "expression": expression, "metadata": {}}
        
        # <ID> = <expr>
        if token["type"] == "ID":
            var_name = token["value"]
            self.advance()
            if self.current_token() and self.current_token()["type"] == "ASSIGN":
                self.advance()
                expression = self.parse_expression()
                self.consume_newline()
                return {"type": "AssignmentStatement", "name": var_name, "expression": expression, "metadata": {}}
            else:
                # Se for apenas um ID solto, pode ser erro ou expressão isolada (não suportada como statement aqui)
                raise RuntimeError(f"Esperado '=' após identificador '{var_name}'")
        
        return None

    def consume_newline(self):
        if self.current_token() and self.current_token()["type"] == "NEWLINE":
            self.advance()

    def parse_expression(self):
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
        token = self.current_token()
        if not token: return None
            
        if token["type"] == "NUMBER":
            self.advance()
            return {"type": "LiteralNumber", "metadata": {"value": token["value"]}}
        
        if token["type"] == "ID":
            self.advance()
            return {"type": "VariableReference", "metadata": {"name": token["value"]}}
        
        if token["type"] == "LPAREN":
            self.advance()
            node = self.parse_expression()
            if self.current_token() and self.current_token()["type"] == "RPAREN":
                self.advance()
                return node
            else:
                raise RuntimeError("Esperado ')'")
                
        raise RuntimeError(f"Token inesperado: {token['value']}")
