import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Mini SIEM",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= LOAD CSS =================
css_path = os.path.join(os.path.dirname(__file__), "style.css")
with open(css_path, "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ================= BASE64 IMAGE LOADER =================
def load_image_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

TOP_IMG = load_image_b64(os.path.join(BASE_DIR, "assets", "marquee", "TOP_IMG.png"))
BOTTOM_IMG = load_image_b64(os.path.join(BASE_DIR, "assets", "marquee", "BOTTOM_IMG.png"))

# ================= FULL-WIDTH INFINITE MARQUEE =================
st.markdown(f"""
<div class="marquee-container">
  <div class="marquee-track">
    <div class="marquee-segment">
      <img src="data:image/png;base64,{TOP_IMG}">
      <img src="data:image/png;base64,{BOTTOM_IMG}">
      <img src="data:image/png;base64,{TOP_IMG}">
      <img src="data:image/png;base64,{BOTTOM_IMG}">
    </div>
    <div class="marquee-segment">
      <img src="data:image/png;base64,{TOP_IMG}">
      <img src="data:image/png;base64,{BOTTOM_IMG}">
      <img src="data:image/png;base64,{TOP_IMG}">
      <img src="data:image/png;base64,{BOTTOM_IMG}">
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("<h1 class='title'>AI-Powered Mini SIEM</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>SOC-style alerting, correlation & ML-assisted anomaly detection</p>", unsafe_allow_html=True)

# ================= LOAD DATA =================
DATA_PATH = os.path.join(BASE_DIR, "backend", "data", "demo_events.csv")
df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"])

# ================= ALERT CONSOLE + DRILLDOWN =================
left, right = st.columns([3, 2])

with left:
    st.subheader("📋 Alert Console")
    st.dataframe(
        df.sort_values("timestamp", ascending=False),
        use_container_width=True,
        height=420
    )

with right:
    st.subheader("🔎 Alert Drill-Down")
    idx = st.selectbox(
        "Select Alert",
        range(len(df)),
        format_func=lambda i: f"Alert #{i} — {df.iloc[i]['severity']} — {df.iloc[i]['event_type']}"
    )
    st.json(df.iloc[idx].to_dict())

# ================= CORRELATION RULES =================
st.subheader("🧩 Correlation Rules Engine")
st.markdown("""
<div class="rules-box">
<ul>
<li><b>Deauthentication burst + handshake activity</b> → WPA2 exploitation attempt</li>
<li><b>Repeated source MAC</b> within short window</li>
<li><b>High ML anomaly score</b> combined with protocol misuse</li>
<li><b>Cross-access-point alert correlation</b></li>
</ul>
<p class="muted">
Enterprise SOC-style correlation logic inspired by RSA NetWitness.
</p>
</div>
""", unsafe_allow_html=True)

# ================= ML ANOMALY SCORES =================
st.subheader("🧠 ML Anomaly Scores")
fig_anomaly = px.scatter(
    df,
    x="timestamp",
    y="anomaly_score",
    color="severity",
    template="plotly_dark",
    height=360
)
st.plotly_chart(fig_anomaly, use_container_width=True)

# ================= EVENTS OVER TIME =================
st.subheader("📈 Events Over Time")
events_ts = (
    df.groupby(df["timestamp"].dt.floor("min"))
      .size()
      .reset_index(name="count")
)
fig_ts = px.line(events_ts, x="timestamp", y="count", template="plotly_dark", height=330)
st.plotly_chart(fig_ts, use_container_width=True)

# ================= METRICS =================
st.divider()
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Events", len(df))
m2.metric("Critical Alerts", int((df["severity"] == "CRITICAL").sum()))
m3.metric("High Severity Alerts", int((df["severity"] == "HIGH").sum()))
m4.metric("Avg Anomaly Score", round(float(df["anomaly_score"].mean()), 2))

# ================= PIE CHART (BOTTOM) =================
st.subheader("🚨 Alert Severity Distribution")
fig_pie = px.pie(df, names="severity", hole=0.6, template="plotly_dark")
st.plotly_chart(fig_pie, use_container_width=True)

# ================= BOTTOM QUOTE =================
st.markdown("""
<div class="bottom-panel">
<p class="quote">
“Did you know? With less than ₹5000, attackers can exploit unauthenticated 802.11 deauthentication frames to disrupt Wi-Fi and force reconnections.”
</p>
</div>
""", unsafe_allow_html=True)
