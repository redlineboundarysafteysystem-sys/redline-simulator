import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta

st.set_page_config(page_title="RedLINE Simulator", layout="centered")

st.title("🔴🟠🟢 RedLINE — Upstream Timing Deviation Detector")
st.markdown("**Environmental Boundary and Timing Deviation Detection System** (Provisional Patent Pending)")

st.subheader("Watch the dots move + timestamps stretch in real time")

html_demo = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RedLINE Animated Demo</title>
  <style>
    body { font-family: system-ui, -apple-system, sans-serif; background:#0f0f12; color:#e0e0e0; padding:20px; margin:0; }
    .card { max-width:720px; margin:0 auto; background:#1a1a1f; border-radius:20px; padding:40px; box-shadow:0 15px 40px rgba(0,0,0,0.7); }
    h1 { text-align:center; font-size:32px; margin-bottom:8px; }
    .subtitle { text-align:center; color:#aaa; font-size:18px; margin-bottom:30px; }
    .timeline { display:flex; justify-content:space-between; align-items:center; margin:40px 0; position:relative; }
    .timeline::before { content:''; position:absolute; top:50%; left:10px; right:10px; height:6px; background:#333; z-index:1; border-radius:3px; }
    .dot { width:32px; height:32px; border-radius:50%; background:#555; position:relative; z-index:2; transition:all 0.7s ease; box-shadow:0 4px 12px rgba(0,0,0,0.5); }
    .dot.active { transform:scale(1.4); }
    .dot.stable { background:#4ade80; box-shadow:0 0 20px #4ade80; }
    .dot.shifting { background:#fbbf24; box-shadow:0 0 20px #fbbf24; }
    .dot.drifting { background:#f87171; box-shadow:0 0 20px #f87171; }
    .labels { display:flex; justify-content:space-between; font-size:14px; color:#888; margin-top:8px; }
    .timestamps { display:flex; justify-content:space-between; font-family: monospace; font-size:14px; color:#bbb; margin-top:12px; }
    button { background:#3b82f6; color:white; border:none; padding:16px 40px; font-size:18px; border-radius:12px; cursor:pointer; display:block; margin:40px auto; }
    button:hover { background:#2563eb; }
    .message { min-height:110px; padding:20px; background:#222; border-radius:12px; font-size:17px; line-height:1.5; margin-top:20px; }
  </style>
</head>
<body>
<div class="card">
  <h1>Timing shifts upstream</h1>
  <div class="subtitle">Problems show up downstream</div>

  <div class="timeline" id="timeline">
    <div class="dot" id="d1"></div>
    <div class="dot" id="d2"></div>
    <div class="dot" id="d3"></div>
    <div class="dot" id="d4"></div>
    <div class="dot" id="d5"></div>
    <div class="dot" id="d6"></div>
    <div class="dot" id="d7"></div>
    <div class="dot" id="d8"></div>
  </div>

  <div class="labels">
    <div>Stable</div>
    <div>Shifting begins</div>
    <div>Drift forming</div>
  </div>

  <div class="timestamps" id="timestamps">
    <div id="t1">10:00</div><div id="t2">10:05</div><div id="t3">10:10</div><div id="t4">10:15</div>
    <div id="t5">10:20</div><div id="t6">10:26</div><div id="t7">10:34</div><div id="t8">10:45</div>
  </div>

  <button onclick="runDemo()">🚀 Start RedLINE Demo</button>

  <div id="message" class="message">Press the button to watch the cadence stretch in real time.</div>
</div>

<script>
const dots = [document.getElementById('d1'),document.getElementById('d2'),document.getElementById('d
