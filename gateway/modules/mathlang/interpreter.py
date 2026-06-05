from framework.interfaces import BaseInterpreter

class MathLangInterpreter(BaseInterpreter):
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
            
            if isinstance(result, float) and result.is_integer():
                result = int(result)
                
            prefix = "[MathLang Output]"
            if ast.get("metadata", {}).get("optimized"):
                prefix = f"{prefix} (OPTIMIZED)"
                
            return f"{prefix}: {result}"
        except Exception as e:
            return f"Erro de execução: {e}"
