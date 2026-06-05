from flask import Flask, request, jsonify
import os

app = Flask(__name__)

class PythonBackend:
    """Executa a AST usando eval do Python"""
    @staticmethod
    def execute(ast):
        tokens = ast.get("tokens", [])
        if not tokens:
            raise ValueError("Nenhum token para executar")
        
        expression = " ".join(str(t) for t in tokens)
        
        # Validação de segurança (simples - em produção seria mais robusto)
        dangerous_keywords = ["import", "open", "exec", "eval", "__"]
        if any(keyword in expression.lower() for keyword in dangerous_keywords):
            raise ValueError("Expressão contém operações perigosas")
        
        result = eval(expression)
        return str(result)

@app.route('/execute', methods=['POST'])
def execute():
    try:
        data = request.get_json()
        ast = data.get("ast", {})
        
        if not ast:
            return jsonify({"success": False, "error": "AST vazia"}), 400
        
        result = PythonBackend.execute(ast)
        
        return jsonify({
            "success": True,
            "result": result,
            "execution_time_ms": 0
        })
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Erro na execução: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "backend-service"}), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5004))
    app.run(debug=True, host='0.0.0.0', port=port)
