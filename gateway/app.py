import os
import sys
import logging

# Adiciona a raiz ao path para encontrar o framework
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from framework.engine import CodeWeaverEngine
from framework.service import BaseServiceHandler, start_service
from framework.interfaces import BaseLexer, BaseParser, BaseInterpreter

# Configuração de Log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Gateway")

# --- 🚀 ÁREA DE INJEÇÃO DE HOTSPOTS ---
# Implemente suas classes aqui ou importe-as de módulos externos.

class PlaceholderLexer(BaseLexer):
    def tokenize(self, code):
        return [code] # Implementação dummy

class PlaceholderParser(BaseParser):
    def parse(self, tokens):
        return {"raw": tokens} # Implementação dummy

class PlaceholderInterpreter(BaseInterpreter):
    def execute(self, ast):
        return f"Framework Core Executado. Dados: {ast}"

# --- 🛠️ CONFIGURAÇÃO DA ENGINE ---
# Aqui os Hotspots são conectados ao Frozen Spot (Engine)
engine = CodeWeaverEngine(
    lexer=PlaceholderLexer(), 
    parser=PlaceholderParser(), 
    interpreter=PlaceholderInterpreter(), 
    analyzer_url=os.getenv("ANALYZER_URL", "http://localhost:5001"),
    notifier_url=os.getenv("NOTIFIER_URL", "http://localhost:5002")
)

class GatewayHandler(BaseServiceHandler):
    """
    Handler genérico que delega o processamento para a Engine do Framework.
    """
    def do_GET(self):
        self.send_json({
            "status": "online",
            "framework": "CodeWeaver v1.0",
            "info": "Aguardando injeção de Hotspots no Gateway."
        })

    def do_POST(self):
        if self.path == '/api/compile':
            data = self.get_post_data()
            code = data.get('code', '')
            
            if not code:
                self.send_error(400, "Código não fornecido.")
                return

            # O fluxo é fixo (Frozen Spot), a lógica é variável (Hotspots)
            result = engine.compile_and_run(code)
            self.send_json(result)
        else:
            self.send_error(404)

if __name__ == "__main__":
    # O Gateway sobe na porta 5000 por padrão
    port = int(os.getenv("PORT", 5000))
    start_service(port, GatewayHandler, "CodeWeaver Gateway")
