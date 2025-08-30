from flask import Flask, jsonify
import requests
import threading
import time

app = Flask(__name__)

# 👇 Service A ka URL (without /health)
SERVICE_A_URL = "https://render-service-a.onrender.com"

status_data = {SERVICE_A_URL: "unknown"}

def ping_service_a():
    while True:
        try:
            r = requests.get(SERVICE_A_URL, timeout=10)
            if r.status_code == 200:
                status_data[SERVICE_A_URL] = "ok"
            else:
                status_data[SERVICE_A_URL] = f"error {r.status_code}"
        except Exception:
            status_data[SERVICE_A_URL] = "down"
        time.sleep(300)  # 5 min

@app.route("/health")
def health():
    return jsonify(status_data)

if __name__ == "__main__":
    t = threading.Thread(target=ping_service_a, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=10000)
    
