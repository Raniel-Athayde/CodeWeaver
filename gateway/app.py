import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

# Adiciona a raiz do projeto ao path para importar o framework
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 🏛️ IMPORTAÇÃO DO FRAMEWORK (FROZEN SPOT)
from framework.engine import CodeWeaverEngine

# 🚀 IMPORTAÇÃO DA APLICAÇÃO (HOTSPOT)
from modules.mathlang import MathLangLexer, MathLangParser, MathLangInterpreter

# Instanciação da aplicação usando o framework
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
                file_path = os.path.join(os.path.dirname(__file__), 'index.html')
                with open(file_path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, f"Erro ao carregar interface: {e}")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/compile':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            # Chama o motor do framework
            result = engine.compile_and_run(data.get('code', ''))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 5000), GatewayHandler)
    print("🚀 Gateway (Aplicação) rodando na porta 5000...")
    print("🏛️ Framework CodeWeaver carregado com sucesso.")
    server.serve_forever()
