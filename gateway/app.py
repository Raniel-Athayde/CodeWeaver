import time
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional

# ==========================================
# ❄️ CORE DO FRAMEWORK (FROZEN SPOTS)
# ==========================================

class Token(BaseModel):
    type: str
    value: str

class ASTNode(BaseModel):
    type: str
    children: List['ASTNode'] = []
    metadata: dict = {}

class ExecutionResult(BaseModel):
    success: bool
    output: str
    execution_time_ms: float

class CodeWeaverEngine:
    def __init__(self, lexer, parser, interpreter, analyzer_url: str):
        self.lexer = lexer
        self.parser = parser
        self.interpreter = interpreter
        self.analyzer_url = analyzer_url

    def compile_and_run(self, source_code: str) -> ExecutionResult:
        start_time = time.time()
        
        # Phase 1: Análise Léxica
        tokens = self.lexer.tokenize(source_code)
        
        # Phase 2: Análise Sintática
        raw_ast = self.parser.parse(tokens)
        
        # Phase 3: Chamada ao Microserviço de Otimização (Network Call)
        try:
            response = requests.post(f"{self.analyzer_url}/optimize", json=raw_ast.dict())
            optimized_ast_data = response.json()
            optimized_ast = ASTNode(**optimized_ast_data)
        except Exception:
            optimized_ast = raw_ast # Fallback se o serviço estiver offline
        
        # Phase 4: Execução
        output = self.interpreter.execute(optimized_ast)
        
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000

        return ExecutionResult(
            success=True,
            output=output,
            execution_time_ms=round(execution_time, 2)
        )

# ==========================================
# 🚀 CUSTOMIZAÇÃO (HOTSPOTS) - MathLang
# ==========================================

class MathLangLexer:
    def tokenize(self, source_code: str) -> List[Token]:
        parts = source_code.strip().split()
        tokens = []
        if parts and parts[0] == "PRINT":
            tokens.append(Token(type="KEYWORD", value="PRINT"))
            if len(parts) > 1:
                tokens.append(Token(type="NUMBER", value=parts[1]))
        return tokens

class MathLangParser:
    def parse(self, tokens: List[Token]) -> ASTNode:
        if not tokens: return ASTNode(type="Empty")
        node = ASTNode(type="PrintStatement")
        for t in tokens:
            if t.type == "NUMBER":
                node.children.append(ASTNode(type="LiteralNumber", metadata={"value": t.value}))
        return node

class MathLangInterpreter:
    def execute(self, ast: ASTNode) -> str:
        if ast.type == "PrintStatement" and ast.children:
            return f"[MathLang Output]: {ast.children[0].metadata.get('value')}"
        return "Nada a executar."

# ==========================================
# 🌐 API GATEWAY & WEB INTERFACE
# ==========================================

app = FastAPI()
templates = Jinja2Templates(directory="templates")

engine = CodeWeaverEngine(
    lexer=MathLangLexer(),
    parser=MathLangParser(),
    interpreter=MathLangInterpreter(),
    analyzer_url="http://localhost:5001"
)

class Submission(BaseModel):
    code: str

@app.post("/api/compile")
def compile_code(sub: Submission):
    return engine.compile_and_run(sub.code)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
