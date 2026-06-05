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

class MathLangParser:
    def parse(self, tokens):
        # Estrutura básica: PRINT <expresso>
        # Onde <expressao> pode ser: NUMBER ou NUMBER OPERATOR NUMBER
        ast = {"type": "PrintStatement", "children": [], "metadata": {}}
        
        if not tokens or tokens[0]["type"] != "KEYWORD":
            return ast

        # Pula o PRINT e olha o resto
        expr_tokens = tokens[1:]
        
        if len(expr_tokens) == 1:
            # Apenas um número: PRINT 100
            ast["children"].append({
                "type": "LiteralNumber", 
                "metadata": {"value": expr_tokens[0]["value"]}
            })
        elif len(expr_tokens) >= 3:
            # Expressão binária: PRINT 10 + 20
            ast["children"].append({
                "type": "BinaryExpression",
                "metadata": {"operator": expr_tokens[1]["value"]},
                "children": [
                    {"type": "LiteralNumber", "metadata": {"value": expr_tokens[0]["value"]}},
                    {"type": "LiteralNumber", "metadata": {"value": expr_tokens[2]["value"]}}
                ]
            })
        return ast

class MathLangInterpreter:
    def execute(self, ast):
        if ast["type"] != "PrintStatement" or not ast["children"]:
            return "Erro: Comando inválido."

        child = ast["children"][0]
        
        try:
            if child["type"] == "LiteralNumber":
                result = float(child["metadata"]["value"])
            elif child["type"] == "BinaryExpression":
                op = child["metadata"]["operator"]
                v1 = float(child["children"][0]["metadata"]["value"])
                v2 = float(child["children"][1]["metadata"]["value"])
                
                if op == "+": result = v1 + v2
                elif op == "-": result = v1 - v2
                elif op == "*": result = v1 * v2
                elif op == "/": result = v1 / v2 if v2 != 0 else "Erro: Divisão por zero"
            
            # Formatação do resultado
            if isinstance(result, float) and result.is_integer():
                result = int(result)
                
            prefix = "[MathLang Output]"
            if ast.get("metadata", {}).get("optimized"):
                prefix = f"{prefix} (OPTIMIZED)"
                
            return f"{prefix}: {result}"
        except Exception as e:
            return f"Erro de execução: {e}"
