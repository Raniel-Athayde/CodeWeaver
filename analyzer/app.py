from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Microserviço de Análise")

class ASTNode(BaseModel):
    type: str
    children: list = []
    metadata: dict = {}

@app.post("/optimize")
def optimize(ast: ASTNode):
    # Lógica de otimização simulada
    if ast.type == "PrintStatement":
        ast.metadata["optimized"] = True
        ast.metadata["service_info"] = "Análise semântica realizada via microserviço"
    return ast

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
