from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random
import uvicorn

app = FastAPI()

# Bikin 3 Metrik (Syarat Kriteria 4)
REQUEST_COUNT = Counter('app_requests_total', 'Total request ke model', ['method', 'endpoint'])
ERROR_COUNT = Counter('app_errors_total', 'Total error yang terjadi')
LATENCY = Histogram('app_latency_seconds', 'Waktu proses request (detik)')

@app.post("/predict")
def predict():
    start_time = time.time()
    REQUEST_COUNT.labels(method='POST', endpoint='/predict').inc()
    
    # Simulasi proses model Machine Learning (delay random)
    time.sleep(random.uniform(0.1, 0.5))
    
    # Simulasi error (10% kemungkinan error)
    if random.random() < 0.1:
        ERROR_COUNT.inc()
        return {"status": "error", "message": "Model gagal memproses data"}

    latency = time.time() - start_time
    LATENCY.observe(latency)
    
    return {"status": "success", "prediction": random.choice([0, 1])}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    print("Server Model berjalan di http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)