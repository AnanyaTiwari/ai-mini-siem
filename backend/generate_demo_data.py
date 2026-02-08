"""
Generate realistic SIEM-style demo telemetry
"""

import pandas as pd
import random
from datetime import datetime, timedelta

OUTPUT_FILE = "backend/data/demo_events.csv"

SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
EVENT_TYPES = [
    "Authentication Failure",
    "Suspicious DNS Query",
    "Port Scan Detected",
    "Deauthentication Burst",
    "Handshake Capture Attempt",
    "Brute Force Attempt"
]

def generate_events(num_events=400):
    now = datetime.now()
    rows = []

    for i in range(num_events):
        timestamp = now - timedelta(minutes=num_events - i)

        severity = random.choices(
            SEVERITIES, weights=[60, 25, 10, 5]
        )[0]

        anomaly_score = round(random.uniform(0.1, 1.0), 2)
        if severity in ["HIGH", "CRITICAL"]:
            anomaly_score = round(random.uniform(0.75, 1.0), 2)

        rows.append({
            "timestamp": timestamp,
            "source_ip": f"192.168.1.{random.randint(2,254)}",
            "destination_ip": f"10.0.0.{random.randint(2,254)}",
            "event_type": random.choice(EVENT_TYPES),
            "severity": severity,
            "anomaly_score": anomaly_score,
            "status": "OPEN"
        })

    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = generate_events()
    df.to_csv(OUTPUT_FILE, index=False)
    print("[+] Demo SIEM data generated:", OUTPUT_FILE)
