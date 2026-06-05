import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class BaseServiceHandler(BaseHTTPRequestHandler):
    """
    Handler genérico para microserviços do framework.
    Cuida da leitura de JSON e envio de respostas.
    """
    def get_post_data(self):
        content_length = int(self.headers['Content-Length'])
        return json.loads(self.rfile.read(content_length))

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def start_service(port, handler_class, name):
    server = HTTPServer(('0.0.0.0', port), handler_class)
    print(f"✅ {name} rodando na porta {port}...")
    server.serve_forever()
