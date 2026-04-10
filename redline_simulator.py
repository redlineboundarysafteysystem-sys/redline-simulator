import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="RedLINE Simulator", layout="centered")

st.title("🔴🟠🟢 RedLINE — Upstream Timing Deviation Detector")
st.markdown("**Environmental Boundary and Timing Deviation Detection System** (Provisional Patent Pending)")

st.subheader("Watch the dots move and phases change in real time")

html_demo = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RedLINE Animated Demo</title>
  <style>
    body { font-family: system-ui, sans-serif; background: #0f0f12; color: #e0e0e0; padding: 20px; margin: 0; }
    .container { max-width: 700px; margin: 0 auto; background: #1a1a1f; border-radius: 16px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.5); }
    .title { font-size: 28px; font-weight: 700; text-align: center; margin-bottom: 8px; }
    .subtitle { text-align: center; color: #aaa; margin-bottom: 30px; }
    .timeline { display: flex; justify-content: space-between; align-items: center; margin: 40px 0; position: relative; }
    .timeline::before { content: ''; position: absolute; top: 50%; left: 0; right: 0; height: 4px; background: #333; z-index: 1; }
    .dot { width: 24px; height: 24px; border-radius: 50%; background: #444; position: relative; z-index: 2; transition: all 0.6s ease; }
    .dot.active { transform: scale(1.3); box-shadow: 0 0 15px currentColor; }
    .dot.stable { background: #4ade80; }
    .dot.shifting { background: #fbbf24; }
    .dot.drifting { background: #f87171; }
    .phase { text-align: center; font-size: 15px; margin-top: 8px; }
    button { background: #3b82f6; color: white; border: none; padding: 14px 32px; font-size: 17px; border-radius: 10px; cursor: pointer; display: block; margin: 30px auto; }
    button:hover { background: #2563eb; }
    .message { min-height: 80px; padding: 16px; background: #222; border-radius: 10px; margin-top: 20px; font-size: 16px; }
  </style>
</head>
<body>
<div class="container">
  <div class="title">RedLINE — Timing Shifts Upstream</div>
  <div class="subtitle">Problems show up downstream. RedLINE sees the change early.</div>

  <div id="timeline" class="timeline">
    <div class="dot stable" id="dot1"></div>
    <div class="dot stable" id="dot2"></div>
    <div class="dot stable" id="dot3"></div>
    <div class="dot stable" id="dot4"></div>
    <div class="dot" id="dot5"></div>
    <div class="dot" id="dot6"></div>
    <div class="dot" id="dot7"></div>
    <div class="dot" id="dot8"></div>
  </div>

  <div style="display: flex; justify-content: space-around; font-size: 13px; color: #888; margin-bottom: 20px;">
    <div>Stable</div>
    <div>Shifting</div>
    <div>Drifting</div>
  </div>

  <button onclick="runDemo()">🚀 Run Animated Demo</button>

  <div id="message" class="message">Click the button to watch the upstream shift happen in real time.</div>
</div>

<script>
const dots = [
  document.getElementById('dot1'),
  document.getElementById('dot2'),
  document.getElementById('dot3'),
  document.getElementById('dot4'),
  document.getElementById('dot5'),
  document.getElementById('dot6'),
  document.getElementById('dot7'),
  document.getElementById('dot8')
];

const messageEl = document.getElementById('message');

function runDemo() {
  // Reset
  dots.forEach(d => d.className = 'dot');
  messageEl.textContent = 'Starting simulation...';

  let step = 0;
  const phases = [
    "🟢 Cadence is stable. Spacing is consistent.",
    "🟢 Cadence is stable. Spacing is consistent.",
    "🟠 The spacing is beginning to stretch. Early shift detected.",
    "🟠 The spacing is beginning to stretch. Early shift detected.",
    "🟠 Shifting phase — visible failure still ahead.",
    "🔴 Drift is forming before visible failure.",
    "🔴 Drift is forming before visible failure.",
    "🔴 This is the upstream window RedLINE is built to reveal."
  ];

  const interval = setInterval(() => {
    if (step < dots.length) {
      dots[step].classList.add('active');
      if (step >= 4) dots[step].classList.add('shifting');
      if (step >= 6) dots[step].classList.add('drifting');
      
      messageEl.textContent = phases[Math.min(step, phases.length-1)];
      step++;
    } else {
      clearInterval(interval);
      messageEl.innerHTML = '<strong>Demo complete.</strong><br>Timing shifts appeared upstream — before any visible downstream problem.<br><br><strong>This is what RedLINE detects.</strong>';
    }
  }, 800); // speed of animation
}
</script>
</body>
</html>
"""

components.html(html_demo, height=700)

st.caption("This is a proof-of-concept animation showing how RedLINE reveals upstream timing deviation.")
