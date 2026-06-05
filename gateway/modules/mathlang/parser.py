from framework.interfaces import BaseParser

class MathLangParser(BaseParser):
    def parse(self, tokens):
        # Estrutura básica: PRINT <expresso>
        ast = {"type": "PrintStatement", "children": [], "metadata": {}}
        
        if not tokens or tokens[0]["type"] != "KEYWORD":
            return ast

        expr_tokens = tokens[1:]
        
        if len(expr_tokens) == 1:
            ast["children"].append({
                "type": "LiteralNumber", 
                "metadata": {"value": expr_tokens[0]["value"]}
            })
        elif len(expr_tokens) >= 3:
            ast["children"].append({
                "type": "BinaryExpression",
                "metadata": {"operator": expr_tokens[1]["value"]},
                "children": [
                    {"type": "LiteralNumber", "metadata": {"value": expr_tokens[0]["value"]}},
                    {"type": "LiteralNumber", "metadata": {"value": expr_tokens[2]["value"]}}
                ]
            })
        return ast
