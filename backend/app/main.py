from fastapi import FastAPI
 
app = FastAPI(
    title="DeporteData API",
    description="Backend API para DeporteData",
    version="0.1.0",
)
 
 
@app.get("/health")
def health_check():
    return {"status": "ok"}