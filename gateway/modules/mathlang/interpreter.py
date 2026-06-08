from framework.interfaces import BaseInterpreter

class MathLangInterpreter(BaseInterpreter):
    def execute(self, ast):
        if ast["type"] != "PrintStatement" or not ast["children"]:
            return "Erro: Comando inválido."

        try:
            result = self.evaluate(ast["children"][0])
            
            if isinstance(result, float) and result.is_integer():
                result = int(result)
                
            prefix = "[MathLang Output]"
            if ast.get("metadata", {}).get("optimized"):
                prefix = f"{prefix} (OPTIMIZED)"
                
            return f"{prefix}: {result}"
        except Exception as e:
            return f"Erro de execução: {e}"

    def evaluate(self, node):
        if node["type"] == "LiteralNumber":
            return float(node["metadata"]["value"])
        
        if node["type"] == "BinaryExpression":
            op = node["metadata"]["operator"]
            left = self.evaluate(node["children"][0])
            right = self.evaluate(node["children"][1])
            
            if op == "+": return left + right
            if op == "-": return left - right
            if op == "*": return left * right
            if op == "/":
                if right == 0:
                    raise RuntimeError("Divisão por zero")
                return left / right
        
        raise RuntimeError(f"Tipo de nó desconhecido: {node['type']}")
