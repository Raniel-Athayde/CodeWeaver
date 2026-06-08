import time
import requests
import logging

# Configuração de Log padrão do Framework
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
logger = logging.getLogger("CodeWeaver")

class CodeWeaverEngine:
    """
    ❄️ FROZEN SPOT: O Core do Framework.
    Define o fluxo de execução (Pipeline) que é invariante.
    """
    def __init__(self, lexer, parser, interpreter, analyzer_url=None, notifier_url=None, exporter_url=None, importer_url=None):
        self.lexer = lexer
        self.parser = parser
        self.interpreter = interpreter
        self.analyzer_url = analyzer_url
        self.notifier_url = notifier_url
        self.exporter_url = exporter_url
        self.importer_url = importer_url

    def import_code(self, file_content_base64):
        if not self.importer_url:
            return {"status": "error", "error": "Importer service not configured"}
        
        try:
            resp = requests.post(f"{self.importer_url}/import", json={"file_content": file_content_base64}, timeout=2)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.error(f"Erro ao importar: {e}")
        
        return {"status": "error", "error": "Failed to contact importer service"}

    def export_code(self, source_code):
        if not self.exporter_url:
            return {"status": "error", "error": "Exporter service not configured"}
        
        try:
            resp = requests.post(f"{self.exporter_url}/export", json={"code": source_code}, timeout=2)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.error(f"Erro ao exportar: {e}")
        
        return {"status": "error", "error": "Failed to contact exporter service"}

    def compile_and_run(self, source_code):
        """
        Executa o pipeline padrão: Tokenização -> Parsing -> Otimização -> Execução -> Notificação.
        """
        start_time = time.time()
        logger.info("Iniciando processamento de código...")
        
        try:
            # 1. Lexer (🔥 Hotspot)
            tokens = self.lexer.tokenize(source_code)
            
            # 2. Parser (🔥 Hotspot)
            ast = self.parser.parse(tokens)
            
            # 3. Microserviço de Otimização (Infraestrutura)
            optimized = False
            if self.analyzer_url:
                ast, optimized = self._optimize(ast)
                
            # 4. Interpreter (🔥 Hotspot)
            output = self.interpreter.execute(ast)
            
            execution_time = (time.time() - start_time) * 1000
            result = {
                "status": "success",
                "output": output,
                "execution_time_ms": round(execution_time, 2),
                "optimized": optimized
            }

            # 5. Microserviço de Notificação (Infraestrutura)
            if self.notifier_url:
                self._notify(output, execution_time)

            logger.info(f"Processamento concluído em {execution_time:.2f}ms")
            return result

        except Exception as e:
            logger.error(f"Erro no pipeline: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "execution_time_ms": round((time.time() - start_time) * 1000, 2)
            }

    def _optimize(self, ast):
        try:
            resp = requests.post(f"{self.analyzer_url}/optimize", json=ast, timeout=2)
            if resp.status_code == 200:
                return resp.json(), True
        except Exception as e:
            logger.warning(f"Otimizador indisponível: {e}. Prosseguindo com AST original.")
        return ast, False

    def _notify(self, output, execution_time):
        try:
            requests.post(f"{self.notifier_url}/notify", json={
                "message": f"Execução via CodeWeaver finalizada.",
                "execution_time": execution_time,
                "output_preview": str(output)[:100]
            }, timeout=1)
        except Exception as e:
            logger.warning(f"Serviço de notificação falhou: {e}")
