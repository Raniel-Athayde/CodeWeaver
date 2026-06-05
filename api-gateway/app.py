from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

# URLs dos microsserviços
LEXER_URL = os.getenv("LEXER_URL", "http://localhost:5001")
PARSER_URL = os.getenv("PARSER_URL", "http://localhost:5002")
OPTIMIZER_URL = os.getenv("OPTIMIZER_URL", "http://localhost:5003")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5004")
ANALYSIS_URL = os.getenv("ANALYSIS_URL", "http://localhost:5005")
NOTIFICATION_URL = os.getenv("NOTIFICATION_URL", "http://localhost:5006")

def log_event(event_type, payload):
    """Notifica o serviço de notificações"""
    try:
        requests.post(f"{NOTIFICATION_URL}/log", json={
            "event_type": event_type,
            "payload": payload
        }, timeout=2)
    except:
        pass

@app.route('/')
def index():
    with open('/app/interface.HTML', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/api/compile', methods=['POST'])
def compile_code():
    """Orquestra o pipeline de compilação através dos microsserviços"""
    try:
        data = request.get_json()
        source_code = data.get("code", "")
        
        if not source_code.strip():
            return jsonify({"success": False, "error": "Código vazio"}), 400
        
        # 1. Lexer Service
        lexer_response = requests.post(f"{LEXER_URL}/tokenize", 
                                       json={"code": source_code})
        lexer_data = lexer_response.json()
        if not lexer_data.get("success"):
            return jsonify(lexer_data), 400
        
        tokens = lexer_data.get("tokens", [])
        
        # 2. Parser Service
        parser_response = requests.post(f"{PARSER_URL}/parse",
                                       json={"tokens": tokens})
        parser_data = parser_response.json()
        if not parser_data.get("success"):
            return jsonify(parser_data), 400
        
        ast = parser_data.get("ast", {})
        
        # 3. Analysis Service (paralelo)
        analysis_response = requests.post(f"{ANALYSIS_URL}/analyze",
                                         json={"ast": ast})
        analysis_data = analysis_response.json()
        
        # 4. Optimizer Service
        optimizer_response = requests.post(f"{OPTIMIZER_URL}/optimize",
                                          json={"ast": ast})
        optimizer_data = optimizer_response.json()
        if not optimizer_data.get("success"):
            return jsonify(optimizer_data), 400
        
        optimized_ast = optimizer_data.get("ast", {})
        
        # 5. Backend Service (Execução)
        backend_response = requests.post(f"{BACKEND_URL}/execute",
                                        json={"ast": optimized_ast})
        backend_data = backend_response.json()
        if not backend_data.get("success"):
            return jsonify(backend_data), 400
        
        result = backend_data.get("result")
        
        # Log de sucesso
        log_event("COMPILATION_SUCCESS", {
            "code_length": len(source_code),
            "result": result
        })
        
        return jsonify({
            "success": True,
            "result": result,
            "tokens": tokens,
            "ast": ast,
            "analysis": analysis_data.get("analysis", {})
        })
        
    except requests.exceptions.RequestException as e:
        log_event("COMPILATION_ERROR", {"error": f"Microsserviço indisponível: {str(e)}"})
        return jsonify({"success": False, "error": f"Erro ao conectar microsserviços: {str(e)}"}), 503
    except Exception as e:
        log_event("COMPILATION_ERROR", {"error": str(e)})
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
