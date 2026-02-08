# AI-Powered Mini SIEM

A frontend-heavy, SOC-style SIEM dashboard inspired by enterprise tools like
RSA NetWitness and Splunk.

## Features
- SOC-style metrics and alert console
- ML-assisted anomaly scoring
- Severity-based alert visualization
- Time-series event correlation

## Tech Stack
- Python
- Streamlit
- Pandas
- Plotly
- Scikit-learn

## How to Run
```bash
python3 backend/generate_demo_data.py
streamlit run frontend/dashboard.py
