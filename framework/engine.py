import time
import requests

class CodeWeaverEngine:
    """
    ❄️ FROZEN SPOT: O Core do Framework.
    Define o fluxo de execução que nunca muda.
    """
    def __init__(self, lexer, parser, interpreter, analyzer_url, notifier_url):
        self.lexer = lexer
        self.parser = parser
        self.interpreter = interpreter
        self.analyzer_url = analyzer_url
        self.notifier_url = notifier_url

    def compile_and_run(self, source_code):
        start_time = time.time()
        
        # 1. Lexer (Hotspot)
        tokens = self.lexer.tokenize(source_code)
        
        # 2. Parser (Hotspot)
        ast = self.parser.parse(tokens)
        
        # 3. Microserviço de Otimização (Infraestrutura do Framework)
        try:
            resp = requests.post(f"{self.analyzer_url}/optimize", json=ast, timeout=2)
            if resp.status_code == 200:
                ast = resp.json()
        except:
            pass # Fallback resiliente
            
        # 4. Interpreter (Hotspot)
        output = self.interpreter.execute(ast)
        
        execution_time = (time.time() - start_time) * 1000
        
        # 5. Microserviço de Notificação (Infraestrutura do Framework)
        try:
            requests.post(f"{self.notifier_url}/notify", json={
                "message": f"Código processado via Framework em {execution_time:.2f}ms",
                "output": output
            }, timeout=1)
        except:
            pass

        return {
            "output": output,
            "execution_time_ms": round(execution_time, 2)
        }
