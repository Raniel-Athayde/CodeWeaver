import os
import sys

# Adiciona a raiz ao path para encontrar o framework
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from framework.engine import CodeWeaverEngine
from framework.service import BaseServiceHandler, start_service

# O Gateway na branch 'framework' serve como um esqueleto.
# As implementações de Lexer, Parser e Interpreter devem ser injetadas aqui.

class GatewayHandler(BaseServiceHandler):
    def do_GET(self):
        self.send_json({"status": "Framework Ready", "message": "Inject your hotspots to start."})

    def do_POST(self):
        if self.path == '/api/compile':
            self.send_error(501, "Not Implemented: Inject Lexer/Parser/Interpreter")

if __name__ == "__main__":
    start_service(5000, GatewayHandler, "Gateway Framework")
