from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Microserviço de Notificação")

class Notification(BaseModel):
    message: str

@app.post("/notify")
def notify(notif: Notification):
    print(f"📢 [NOTIFICADOR]: {notif.message}")
    return {"status": "success", "message": "Notificação processada"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
