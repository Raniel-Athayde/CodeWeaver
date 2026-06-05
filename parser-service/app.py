from flask import Flask, request, jsonify
import os

app = Flask(__name__)

class SimpleMathParser:
    """Transforma tokens em AST (Abstract Syntax Tree)"""
    @staticmethod
    def parse(tokens):
        if not tokens:
            raise ValueError("Nenhum token para processar")
        
        ast = {
            "type": "Expression",
            "tokens": tokens,
            "operator_count": sum(1 for t in tokens if t in ['+', '-', '*', '/', '%', '//']),
            "operand_count": len(tokens) - sum(1 for t in tokens if t in ['+', '-', '*', '/', '%', '//'])
        }
        return ast

@app.route('/parse', methods=['POST'])
def parse():
    try:
        data = request.get_json()
        tokens = data.get("tokens", [])
        
        if not tokens:
            return jsonify({"success": False, "error": "Nenhum token fornecido"}), 400
        
        ast = SimpleMathParser.parse(tokens)
        
        return jsonify({
            "success": True,
            "ast": ast,
            "tree_depth": 2
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "parser-service"}), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5002))
    app.run(debug=True, host='0.0.0.0', port=port)
