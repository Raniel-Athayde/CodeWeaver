import json
import time
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# ==========================================
# ❄️ CORE DO FRAMEWORK (FROZEN SPOTS)
# ==========================================

class CodeWeaverEngine:
    def __init__(self, lexer, parser, interpreter, analyzer_url, notifier_url):
        self.lexer = lexer
        self.parser = parser
        self.interpreter = interpreter
        self.analyzer_url = analyzer_url
        self.notifier_url = notifier_url

    def compile_and_run(self, source_code):
        start_time = time.time()
        
        # 1. Lexer
        tokens = self.lexer.tokenize(source_code)
        # 2. Parser
        ast = self.parser.parse(tokens)
        
        # 3. Microserviço (Optimizer)
        try:
            resp = requests.post(f"{self.analyzer_url}/optimize", json=ast)
            if resp.status_code == 200:
                ast = resp.json()
        except:
            pass # Fallback
            
        # 4. Interpreter
        output = self.interpreter.execute(ast)
        
        execution_time = (time.time() - start_time) * 1000
        
        # 5. Microserviço (Notifier)
        try:
            requests.post(f"{self.notifier_url}/notify", json={
                "message": f"Código processado com sucesso em {execution_time:.2f}ms",
                "output": output
            })
        except:
            pass

        return {
            "output": output,
            "execution_time_ms": round(execution_time, 2)
        }

# ==========================================
# 🚀 CUSTOMIZAÇÃO (HOTSPOTS)
# ==========================================

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
            
            # Verifica se foi otimizado pelo microserviço
            prefix = "[MathLang Output]"
            if ast.get("metadata", {}).get("optimized"):
                prefix = f"{prefix} (OPTIMIZED)"
                
            return f"{prefix}: {val}"
        return "Comando não reconhecido."

# ==========================================
# 🌐 GATEWAY SERVER
# ==========================================

engine = CodeWeaverEngine(
    MathLangLexer(), 
    MathLangParser(), 
    MathLangInterpreter(), 
    "http://localhost:5001",
    "http://localhost:5002"
)

class GatewayHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            try:
                # Tenta ler o arquivo index.html na mesma pasta
                file_path = os.path.join(os.path.dirname(__file__), 'index.html')
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, f"Erro ao carregar index.html: {e}")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/compile':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            result = engine.compile_and_run(data.get('code', ''))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 5000), GatewayHandler)
    print("Gateway rodando na porta 5000...")
    server.serve_forever()
