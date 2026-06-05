import os
import sys

# Adiciona a raiz ao path para encontrar o framework
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from framework.service import BaseServiceHandler, start_service

class NotifierHandler(BaseServiceHandler):
    def do_POST(self):
        if self.path == '/notify':
            data = self.get_post_data()
            print(f"📢 [NOTIFICADOR]: {data.get('message')}")
            self.send_json({"status": "ok"})

if __name__ == "__main__":
    start_service(5002, NotifierHandler, "Notifier")
