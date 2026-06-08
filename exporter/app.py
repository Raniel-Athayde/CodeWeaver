import os
import sys

# Adiciona a raiz ao path para encontrar o framework
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from framework.service import BaseServiceHandler, start_service

class ExporterHandler(BaseServiceHandler):
    def do_POST(self):
        if self.path == '/export':
            data = self.get_post_data()
            code = data.get('code', '')
            
            # Simula a geração de um arquivo (aqui apenas retornamos o conteúdo)
            # Em um cenário real, poderíamos salvar no disco ou S3
            response = {
                "filename": "codigo_fonte.txt",
                "content": code
            }
            
            self.send_json(response)

if __name__ == "__main__":
    start_service(5003, ExporterHandler, "Exporter Service")
