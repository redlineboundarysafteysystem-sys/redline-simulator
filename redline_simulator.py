import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="RedLINE Simulator", layout="centered")

st.title("🔴🟠🟢 RedLINE — Upstream Timing Deviation Detector")
st.markdown("**Environmental Boundary and Timing Deviation Detection System** (Provisional Patent Pending)")

st.subheader("Watch the upstream timing shift in action")

# Your original animated demo (the one from the video)
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RedLINE Demo</title>
  <style>
    body { font-family: system-ui, sans-serif; background: #0f0f12; color: #e0e0e0; padding: 20px; }
    .card { max-width: 620px; margin: 0 auto; background: #1a1a1f; border-radius: 16px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
    .big { font-size: 28px; font-weight: 700; line-height: 1.2; margin-bottom: 12px; }
    .muted { color: #888; font-size: 15px; }
    table { width: 100%; border-collapse: collapse; margin-top: 12px; }
    th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #333; }
    th { color: #888; font-weight: 500; }
    .state-normal { color: #4ade80; }
    .state-warning { color: #fbbf24; }
    .state-critical { color: #f87171; font-weight: 600; }
    button { background: #3b82f6; color: white; border: none; padding: 14px 28px; border-radius: 8px; font-size: 17px; cursor: pointer; margin-top: 20px; }
    button:hover { background: #2563eb; }
    .status { margin-top: 16px; padding: 12px; background: #222; border-radius: 8px; min-height: 50px; }
  </style>
</head>
<body>
<div class="card">
  <div class="big">Timing shifts upstream.<br>Problems show up downstream.</div>
  <div class="muted">This is not a finished product — it's proof of the behavior RedLINE detects.</div>

  <div style="margin-top:28px; font-weight:600;">Event spacing (live simulation)</div>
  <table id="intervalTable">
    <thead><tr><th>#</th><th>Time</th><th>Gap</th><th>State</th></tr></thead>
    <tbody id="tableBody"></tbody>
  </table>

  <div class="status" id="status">Click "Simulate Upstream Shift" to start the demo</div>
  <button onclick="runSimulation()">🚀 Simulate Upstream Shift</button>
</div>

<script>
let eventCount = 0;
const tbody = document.getElementById('tableBody');
const statusEl = document.getElementById('status');

function addEvent(gap) {
  eventCount++;
  const time = new Date().toLocaleTimeString('en-US', {hour12: false, hour:"2-digit", minute:"2-digit", second:"2-digit"});
  let stateHTML = '';
  let stateClass = '';

  if (gap > 1800) { stateHTML = 'Stable'; stateClass = 'state-normal'; }
  else if (gap > 1100) { stateHTML = 'Shifting'; stateClass = 'state-warning'; }
  else { stateHTML = 'Drifting — Upstream shift detected'; stateClass = 'state-critical'; }

  const row = document.createElement('tr');
  row.innerHTML = `<td>${eventCount}</td><td>${time}</td><td>${gap} ms</td><td class="${stateClass}">${stateHTML}</td>`;
  tbody.appendChild(row);
  tbody.scrollTop = tbody.scrollHeight;
}

function runSimulation() {
  tbody.innerHTML = '';
  eventCount = 0;
  statusEl.textContent = 'Running simulation...';

  let base = 2200;
  let i = 0;

  const id = setInterval(() => {
    i++;
    const tightening = Math.max(0, Math.floor((i - 6) * 180));
    let gap = base - tightening;
    gap = Math.max(650, gap);

    addEvent(gap);

    if (i >= 12) {
      clearInterval(id);
      statusEl.innerHTML = '<strong>Demo complete.</strong><br>Notice how the gaps started tightening <em>before</em> the critical state appeared.<br><br><strong>This is the upstream window RedLINE reveals.</strong>';
    }
  }, 450);
}
</script>
</body>
</html>
"""

components.html(html_code, height=800, scrolling=True)

st.caption("RedLINE — Provisional Patent Pending • This is a proof-of-concept demo showing upstream timing detection.")
