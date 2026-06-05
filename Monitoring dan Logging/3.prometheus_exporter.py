from flask import Flask, request, Response, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# Bikin 3 Metrik (Syarat Kriteria 4)
REQUEST_COUNT = Counter('app_requests_total', 'Total request ke model', ['method', 'endpoint'])
ERROR_COUNT = Counter('app_errors_total', 'Total error yang terjadi')
LATENCY = Histogram('app_latency_seconds', 'Waktu proses request (detik)')

@app.route("/predict", methods=["POST"])
def predict():
    start_time = time.time()
    REQUEST_COUNT.labels(method='POST', endpoint='/predict').inc()
    
    try:
        data = request.json
        if not data or 'features' not in data:
            raise ValueError("Data cacat atau tidak ada 'features'")
            
        features = data['features']
        # Simulasi prediksi sederhana
        prediction = 1 if sum(features) > 10 else 0
        
        latency = time.time() - start_time
        LATENCY.observe(latency)
        return jsonify({"status": "success", "prediction": prediction})
        
    except Exception as e:
        ERROR_COUNT.inc()
        latency = time.time() - start_time
        LATENCY.observe(latency)
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/metrics", methods=["GET"])
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    print("Server Model Flask berjalan di http://localhost:8000")
    app.run(host="0.0.0.0", port=8000)