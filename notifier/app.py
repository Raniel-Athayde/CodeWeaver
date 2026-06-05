import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class NotifierHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/notify':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            print(f"📢 [NOTIFICADOR]: {data.get('message')}")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 5002), NotifierHandler)
    print("Notifier rodando na porta 5002...")
    server.serve_forever()
