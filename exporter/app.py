import os
import sys

# Adiciona a raiz ao path para encontrar o framework
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from framework.service import BaseServiceHandler, start_service


# ---------------------------------------------------------------------------
# Conversor: AST MathLang → código Python
# ---------------------------------------------------------------------------

def ast_to_python(ast):
    """
    Percorre a AST gerada pelo MathLangParser e produz código Python equivalente.
    """
    if ast.get("type") != "Program":
        raise ValueError("AST inválida: esperado nó raiz 'Program'")

    lines = []
    for statement in ast.get("body", []):
        lines.append(_emit_statement(statement))

    return "\n".join(lines)


def _emit_statement(node):
    t = node["type"]
    if t == "AssignmentStatement":
        name = node["name"]
        expr = _emit_expression(node["expression"])
        return f"{name} = {expr}"
    if t == "PrintStatement":
        expr = _emit_expression(node["expression"])
        return f"print({expr})"
    raise ValueError(f"Tipo de statement desconhecido: {t}")


def _emit_expression(node):
    t = node["type"]
    if t == "LiteralNumber":
        raw = node["metadata"]["value"]
        # Converte para int se for inteiro, float caso contrário
        num = float(raw)
        return str(int(num)) if num.is_integer() else str(num)
    if t == "VariableReference":
        return node["metadata"]["name"]
    if t == "BinaryExpression":
        op = node["metadata"]["operator"]
        left = _emit_expression(node["children"][0])
        right = _emit_expression(node["children"][1])
        return f"({left} {op} {right})"
    raise ValueError(f"Tipo de expressão desconhecido: {t}")


# ---------------------------------------------------------------------------
# Handler do microserviço
# ---------------------------------------------------------------------------

class ExporterHandler(BaseServiceHandler):
    def do_POST(self):
        # Exportação MathLang → TXT (comportamento original)
        if self.path == '/export':
            data = self.get_post_data()
            code = data.get('code', '')
            self.send_json({
                "filename": "codigo_fonte.txt",
                "content": code
            })

        # Exportação MathLang → Python (.py)
        elif self.path == '/export/python':
            ast = self.get_post_data()
            try:
                python_code = ast_to_python(ast)
                self.send_json({
                    "status": "success",
                    "filename": "codigo.py",
                    "content": python_code
                })
            except Exception as e:
                self.send_json({"status": "error", "error": str(e)}, status=400)


if __name__ == "__main__":
    start_service(5003, ExporterHandler, "Exporter Service")
