from flask import Flask, request, jsonify
import os

app = Flask(__name__)

class SimpleMathLexer:
    """Transforma código em tokens"""
    @staticmethod
    def tokenize(source_code):
        # Simples tokenização para matemática básica
        tokens = source_code.split()
        return tokens

@app.route('/tokenize', methods=['POST'])
def tokenize():
    try:
        data = request.get_json()
        code = data.get("code", "")
        
        if not code.strip():
            return jsonify({"success": False, "error": "Código vazio"}), 400
        
        tokens = SimpleMathLexer.tokenize(code)
        
        return jsonify({
            "success": True,
            "tokens": tokens,
            "count": len(tokens)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "lexer-service"}), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
