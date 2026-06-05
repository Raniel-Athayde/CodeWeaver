class MathLangLexer:
    def tokenize(self, code):
        parts = code.strip().split()
        tokens = []
        if parts and parts[0] == "PRINT":
            tokens.append({"type": "KEYWORD", "value": "PRINT"})
            if len(parts) > 1:
                tokens.append({"type": "NUMBER", "value": parts[1]})
        return tokens

class MathLangParser:
    def parse(self, tokens):
        node = {"type": "PrintStatement", "children": [], "metadata": {}}
        for t in tokens:
            if t["type"] == "NUMBER":
                node["children"].append({"type": "LiteralNumber", "metadata": {"value": t["value"]}})
        return node

class MathLangInterpreter:
    def execute(self, ast):
        if ast["type"] == "PrintStatement" and ast["children"]:
            val = ast["children"][0]["metadata"].get("value", "0")
            prefix = "[MathLang Output]"
            if ast.get("metadata", {}).get("optimized"):
                prefix = f"{prefix} (OPTIMIZED)"
            return f"{prefix}: {val}"
        return "Comando não reconhecido."
