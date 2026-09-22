from fastapi import FastAPI

app = FastAPI(title="UK Regulatory Gateway", version="1.0.0")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Gateway is running successfully"}
