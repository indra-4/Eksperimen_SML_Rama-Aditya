import requests
import time
import random

url = "http://localhost:8000/predict"

print("Mulai menembak request ke server...")
while True:
    try:
        # Simulasi 70% request benar, 30% request cacat untuk memicu error metrik
        if random.random() > 0.3:
            payload = {"features": [random.uniform(0, 5) for _ in range(3)]}
        else:
            payload = {"format_salah": "ini akan memicu error di server"}
            
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code} | Respon: {response.json()}")
    except Exception as e:
        print(f"Gagal koneksi: {e}")
    
    # Jeda 1 detik setiap request
    time.sleep(1)