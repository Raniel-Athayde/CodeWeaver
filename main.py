from abc import ABC, abstractmethod
import json
from flask import Flask, request, jsonify, render_template_string

# ==========================================
# MICROSSERVIÇOS (Simulação de Comunicação)
# ==========================================

class AnalysisMicroservice:
    """Simula um microsserviço que analisa a complexidade do código/AST."""
    @staticmethod
    def analyze_ast(ast: dict) -> dict:
        # Na vida real, isso seria uma chamada HTTP/gRPC para outro serviço
        return {"status": "success", "complexity_score": len(str(ast)), "security_warnings": 0}

class NotificationMicroservice:
    """Simula um microsserviço de mensageria ou log centralizado."""
    @staticmethod
    def send_event(event_type: str, payload: dict):
        # Na vida real, publicaria em uma fila Kafka ou RabbitMQ
        print(f"[MICROSSERVIÇO NOTIFICAÇÃO] Evento: {event_type} | Payload: {payload}")

# ==========================================
# HOTSPOTS (Contratos / Strategy Pattern)
# ==========================================

class LexerStrategy(ABC):
    """Hotspot 1: Como o texto bruto é transformado em tokens."""
    @abstractmethod
    def tokenize(self, source_code: str) -> list:
        pass

class ParserStrategy(ABC):
    """Hotspot 2: Como a lista de tokens forma a Árvore Sintática (AST)."""
    @abstractmethod
    def parse(self, tokens: list) -> dict:
        pass

class OptimizerStrategy(ABC):
    """Hotspot 3: Como a AST é otimizada antes da execução/geração de código."""
    @abstractmethod
    def optimize(self, ast: dict) -> dict:
        pass

class BackendStrategy(ABC):
    """Hotspot 4: Como a AST otimizada é processada (Interpretada ou Compilada)."""
    @abstractmethod
    def execute(self, ast: dict) -> str:
        pass

# ==========================================
# FROZEN SPOT (O Núcleo do Framework)
# ==========================================

class CompilerPipeline:
    """
    Este é o Frozen Spot. O fluxo orquestrado é imutável.
    Ele utiliza o padrão Template Method no fluxo, delegando a lógica aos Hotspots.
    """
    def __init__(self, 
                 lexer: LexerStrategy, 
                 parser: ParserStrategy, 
                 optimizer: OptimizerStrategy, 
                 backend: BackendStrategy):
        # Injeção das dependências (Hotspots)
        self.lexer = lexer
        self.parser = parser
        self.optimizer = optimizer
        self.backend = backend

    def compile_and_run(self, source_code: str) -> dict:
        try:
            # 1. Hotspot 1: Análise Léxica
            tokens = self.lexer.tokenize(source_code)
            
            # 2. Hotspot 2: Análise Sintática
            ast = self.parser.parse(tokens)
            
            # Comunicação com Microsserviço (Análise de Qualidade)
            analysis_result = AnalysisMicroservice.analyze_ast(ast)
            
            # 3. Hotspot 3: Otimização
            optimized_ast = self.optimizer.optimize(ast)
            
            # 4. Hotspot 4: Back-end (Execução/Geração)
            result = self.backend.execute(optimized_ast)
            
            # Comunicação com Microsserviço (Notificação de Sucesso)
            NotificationMicroservice.send_event("COMPILATION_SUCCESS", {"result": result})
            
            return {
                "success": True,
                "result": result,
                "analysis": analysis_result
            }
            
        except Exception as e:
            NotificationMicroservice.send_event("COMPILATION_ERROR", {"error": str(e)})
            return {"success": False, "error": str(e)}

# ==========================================
# IMPLEMENTAÇÕES (Exemplo de uso dos Hotspots)
# ==========================================

class SimpleMathLexer(LexerStrategy):
    def tokenize(self, source_code: str) -> list:
        # Implementação simulada ultra-simples para focar na arquitetura
        return source_code.split()

class SimpleMathParser(ParserStrategy):
    def parse(self, tokens: list) -> dict:
        return {"type": "BinaryOp", "tokens": tokens}

class NoOpOptimizer(OptimizerStrategy):
    def optimize(self, ast: dict) -> dict:
        # Retorna a AST sem otimizações (Passthrough)
        return ast

class PythonEvalBackend(BackendStrategy):
    def execute(self, ast: dict) -> str:
        # Backend interpretado simulando a execução com eval nativo
        expression = " ".join(ast["tokens"])
        return str(eval(expression))

# ==========================================
# INTERFACE WEB (Rotas Flask prontas para consumo)
# ==========================================

app = Flask(__name__)

# Configurando o Framework com nossas implementações concretas
framework = CompilerPipeline(
    lexer=SimpleMathLexer(),
    parser=SimpleMathParser(),
    optimizer=NoOpOptimizer(),
    backend=PythonEvalBackend()
)

@app.route('/api/compile', methods=['POST'])
def api_compile():
    data = request.get_json()
    code = data.get("code", "")
    resultado = framework.compile_and_run(code)
    return jsonify(resultado)

@app.route('/')
def index():
    with open('interface.HTML', 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)