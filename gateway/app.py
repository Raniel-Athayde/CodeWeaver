import os
import sys

# Adiciona a raiz ao path para encontrar o framework
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from framework.engine import CodeWeaverEngine
from framework.service import BaseServiceHandler, start_service

# 🚀 COMPONENTES DA APLICAÇÃO
from modules.mathlang.lexer import MathLangLexer
from modules.mathlang.parser import MathLangParser
from modules.mathlang.interpreter import MathLangInterpreter

# Instalação da engine do framework
engine = CodeWeaverEngine(
    MathLangLexer(), 
    MathLangParser(), 
    MathLangInterpreter(), 
    "http://localhost:5001",
    "http://localhost:5002"
)

class GatewayHandler(BaseServiceHandler):
    def do_GET(self):
        if self.path == '/':
            try:
                file_path = os.path.join(os.path.dirname(__file__), 'index.html')
                with open(file_path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, f"Erro: {e}")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/compile':
            data = self.get_post_data()
            result = engine.compile_and_run(data.get('code', ''))
            self.send_json(result)

if __name__ == "__main__":
    start_service(5000, GatewayHandler, "Gateway Principal")
