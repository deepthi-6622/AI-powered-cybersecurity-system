from scapy.all import sniff, IP, TCP, UDP
import requests
import json
import os

API_URL = 'http://127.0.0.1:5001/predict'
DASHBOARD_LOG = '../dashboard/logs.json'

def extract_features(packet):
    try:
        src_ip = packet[IP].src if IP in packet else "0.0.0.0"
        dst_ip = packet[IP].dst if IP in packet else "0.0.0.0"
        protocol = packet.proto if IP in packet else 0
        length = len(packet)

        # Default ports
        src_port = packet[TCP].sport if TCP in packet else (packet[UDP].sport if UDP in packet else 0)
        dst_port = packet[TCP].dport if TCP in packet else (packet[UDP].dport if UDP in packet else 0)

        # Features as numeric values for model
        features = [length, src_port, dst_port, protocol, len(src_ip), len(dst_ip)]

        return features
    except Exception as e:
        print(f"❌ Feature extraction error: {e}")
        return [0, 0, 0, 0, 0, 0]

def handle_packet(packet):
    features = extract_features(packet)
    print(f"📦 Packet features: {features}")

    try:
        response = requests.post(API_URL, json={'features': features})
        if response.status_code != 200:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return

        data = response.json()
        prediction = data.get('prediction')

        log_entry = {
            'features': features,
            'prediction': prediction
        }

        if os.path.exists(DASHBOARD_LOG):
            try:
                with open(DASHBOARD_LOG, 'r') as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
        else:
            logs = []

        logs.append(log_entry)

        with open(DASHBOARD_LOG, 'w') as f:
            json.dump(logs, f, indent=2)

        print(f"✅ Prediction logged: {prediction}")

    except Exception as e:
        print(f"🔥 Exception: {e}")

print("⚡ Starting real-time network monitoring...")
sniff(prn=handle_packet, store=False)


