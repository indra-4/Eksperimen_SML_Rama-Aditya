import requests
import time

url = "http://localhost:8000/predict"

print("Mulai menembak request ke server...")
while True:
    try:
        response = requests.post(url)
        print(f"Status Code: {response.status_code} | Respon: {response.json()}")
    except Exception as e:
        print(f"Gagal koneksi: {e}")
    
    # Jeda 1 detik setiap request
    time.sleep(1)