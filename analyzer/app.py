import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class AnalyzerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/optimize':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            ast = json.loads(post_data)
            
            # Lógica de otimização
            if ast.get('type') == 'PrintStatement':
                ast['metadata']['optimized'] = True
                ast['metadata']['service_info'] = "Otimizado via Standard Lib Server"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(ast).encode('utf-8'))

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 5001), AnalyzerHandler)
    print("Analyzer rodando na porta 5001...")
    server.serve_forever()
