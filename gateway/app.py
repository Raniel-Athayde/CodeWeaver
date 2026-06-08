import os
import sys
import logging

# Adiciona a raiz ao path para encontrar o framework
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from framework.engine import CodeWeaverEngine
from framework.service import BaseServiceHandler, start_service

# 🚀 COMPONENTES DA APLICAÇÃO (HOTSPOTS)
from modules.mathlang.lexer import MathLangLexer
from modules.mathlang.parser import MathLangParser
from modules.mathlang.interpreter import MathLangInterpreter

# Configuração de Log para a Aplicação
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MathLangApp")

# Instalação da engine do framework com as implementações da MathLang
engine = CodeWeaverEngine(
    lexer=MathLangLexer(), 
    parser=MathLangParser(), 
    interpreter=MathLangInterpreter(), 
    analyzer_url="http://localhost:5001",
    notifier_url="http://localhost:5002",
    exporter_url="http://localhost:5003"
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
                logger.error(f"Erro ao servir index.html: {e}")
                self.send_error(500, f"Erro interno: {e}")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/compile':
            data = self.get_post_data()
            code = data.get('code', '')
            
            # Delega o processamento para a Engine (Frozen Spot)
            result = engine.compile_and_run(code)
            self.send_json(result)
        
        elif self.path == '/api/export':
            data = self.get_post_data()
            code = data.get('code', '')
            
            # Chama o serviço de exportação através da Engine
            result = engine.export_code(code)
            self.send_json(result)

if __name__ == "__main__":
    logger.info("Iniciando Gateway da Aplicação MathLang...")
    start_service(5000, GatewayHandler, "MathLang Gateway")
