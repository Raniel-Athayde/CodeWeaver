from framework.interfaces import BaseInterpreter

class MathLangInterpreter(BaseInterpreter):
    def __init__(self):
        self.variables = {}

    def execute(self, ast):
        if ast["type"] != "Program":
            return "Erro: AST inválida."

        self.variables = {} # Limpa variáveis a cada execução
        outputs = []
        try:
            for statement in ast.get("body", []):
                if statement["type"] == "AssignmentStatement":
                    name = statement["name"]
                    value = self.evaluate(statement["expression"])
                    self.variables[name] = value
                
                elif statement["type"] == "PrintStatement":
                    result = self.evaluate(statement["expression"])
                    
                    if isinstance(result, float) and result.is_integer():
                        result = int(result)
                        
                    prefix = "[MathLang Output]"
                    if statement.get("metadata", {}).get("optimized") or ast.get("metadata", {}).get("optimized"):
                        prefix = f"{prefix} (OPTIMIZED)"
                        
                    outputs.append(f"{prefix}: {result}")
            
            return "\n".join(outputs) if outputs else "Execução finalizada."
            
        except Exception as e:
            return f"Erro de execução: {e}"

    def evaluate(self, node):
        if node["type"] == "LiteralNumber":
            return float(node["metadata"]["value"])
        
        if node["type"] == "VariableReference":
            name = node["metadata"]["name"]
            if name in self.variables:
                return self.variables[name]
            raise RuntimeError(f"Variável não definida: '{name}'")
        
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
