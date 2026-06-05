import os
import sys

# Adiciona a raiz ao path para encontrar o framework
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from framework.service import BaseServiceHandler, start_service

class AnalyzerHandler(BaseServiceHandler):
    def do_POST(self):
        if self.path == '/optimize':
            ast = self.get_post_data()
            
            # Lógica de otimização (Hotspot da Aplicação)
            if ast.get('type') == 'PrintStatement':
                ast.setdefault('metadata', {})
                ast['metadata']['optimized'] = True
                ast['metadata']['service_info'] = "Otimizado via Framework Service"
            
            self.send_json(ast)

if __name__ == "__main__":
    start_service(5001, AnalyzerHandler, "Analyzer")
