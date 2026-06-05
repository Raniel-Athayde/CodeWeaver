from flask import Flask, request, jsonify
import os

app = Flask(__name__)

class CodeAnalyzer:
    """Analisa qualidade, complexidade e segurança da AST"""
    @staticmethod
    def analyze(ast):
        tokens = ast.get("tokens", [])
        operator_count = ast.get("operator_count", 0)
        operand_count = ast.get("operand_count", 0)
        
        analysis = {
            "complexity_score": len(str(ast)),
            "operator_count": operator_count,
            "operand_count": operand_count,
            "token_count": len(tokens),
            "security_warnings": []
        }
        
        # Detecção de problemas
        if any(t in tokens for t in ["import", "open", "exec"]):
            analysis["security_warnings"].append("Operações de I/O detectadas")
        
        if operator_count > 5:
            analysis["security_warnings"].append("Alta complexidade de operadores")
        
        return analysis

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        ast = data.get("ast", {})
        
        if not ast:
            return jsonify({"success": False, "error": "AST vazia"}), 400
        
        analysis = CodeAnalyzer.analyze(ast)
        
        return jsonify({
            "success": True,
            "analysis": analysis
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "analysis-service"}), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5005))
    app.run(debug=True, host='0.0.0.0', port=port)
