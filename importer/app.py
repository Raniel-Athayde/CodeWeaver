import os
import sys
import base64

# Adiciona a raiz ao path para encontrar o framework
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from framework.service import BaseServiceHandler, start_service

class ImporterHandler(BaseServiceHandler):
    def do_POST(self):
        if self.path == '/import':
            try:
                data = self.get_post_data()
                file_content_base64 = data.get('file_content', '')
                
                # Decodifica o conteúdo base64
                decoded_content = base64.b64decode(file_content_base64).decode('utf-8')
                
                self.send_json({
                    "status": "success",
                    "code": decoded_content
                })
            except Exception as e:
                self.send_json({
                    "status": "error",
                    "error": str(e)
                }, status=400)

if __name__ == "__main__":
    start_service(5004, ImporterHandler, "Importer Service")
