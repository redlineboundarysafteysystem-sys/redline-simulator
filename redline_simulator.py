<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>RedLINE Timing Drift Demo</title>
<style>
  :root{
    --bg:#f6f7fb;
    --card:#ffffff;
    --text:#111111;
    --muted:#666666;
    --line:#d9dce5;
    --stable:#1f7a1f;
    --shift:#b8860b;
    --drift:#b22222;
  }
  *{box-sizing:border-box}
  body{
    margin:0;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    background:var(--bg);
    color:var(--text);
  }
  .wrap{
    max-width:980px;
    margin:0 auto;
    padding:24px;
  }
  .hero{ margin-bottom:18px; }
  h1{
    margin:0 0 8px;
    font-size:34px;
    line-height:1.1;
  }
  .sub{
    color:var(--muted);
    font-size:18px;
    max-width:760px;
  }
  .grid{
    display:grid;
    grid-template-columns:1.2fr .8fr;
    gap:18px;
  }
  .card{
    background:var(--card);
    border:1px solid var(--line);
    border-radius:18px;
    padding:18px;
    box-shadow:0 4px 14px rgba(0,0,0,.04);
  }
  .controls{
    display:flex;
    gap:10px;
    flex-wrap:wrap;
    margin-bottom:14px;
  }
  button{
    border:none;
    border-radius:12px;
    padding:12px 16px;
    font-size:16px;
    font-weight:600;
    cursor:pointer;
  }
  .primary{ background:#111; color:#fff; }
  .secondary{ background:#eceff6; color:#111; }
  .legend{
    display:flex;
    gap:14px;
    flex-wrap:wrap;
    margin:8px 0 6px;
    color:var(--muted);
    font-size:14px;
  }
  .dot{
    display:inline-block;
    width:10px;height:10px;border-radius:999px;margin-right:6px;vertical-align:middle;
  }
  .stable{ background:var(--stable); }
  .shift{ background:var(--shift); }
  .drift{ background:var(--drift); }
  .timeline{
    position:relative;
    height:280px;
    border:1px solid var(--line);
    border-radius:16px;
    background:linear-gradient(to bottom,#fff,#fbfcff);
    overflow:hidden;
  }
  .axis{
    position:absolute;
    left:54px; right:20px; top:50%;
    height:4px; background:#d6dae4; border-radius:999px;
  }
  .event{
    position:absolute;
    top:50%;
    width:16px; height:16px; border-radius:999px;
    transform:translate(-50%,-50%);
    border:3px solid #fff;
    box-shadow:0 2px 8px rgba(0,0,0,.12);
  }
  .label{
    position:absolute;
    top:calc(50% + 18px);
    transform:translateX(-50%);
    font-size:12px;
    color:#444;
    white-space:nowrap;
  }
  .phaseBand{
    position:absolute;
    top:28px;
    height:32px;
    border-radius:10px;
    color:#111;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:13px;
    font-weight:700;
    opacity:.92;
  }
  .miniTitle{
    font-size:14px;
    font-weight:700;
    color:var(--muted);
    margin-bottom:10px;
    text-transform:uppercase;
    letter-spacing:.04em;
  }
  table{
    width:100%;
    border-collapse:collapse;
    font-size:15px;
  }
  th,td{
    padding:10px 8px;
    border-bottom:1px solid var(--line);
    text-align:left;
  }
  th{ color:var(--muted); font-size:13px; text-transform:uppercase; letter-spacing:.04em; }
  .pill{
    display:inline-block;
    padding:4px 8px;
    border-radius:999px;
    font-size:12px;
    font-weight:700;
  }
  .pill.stable{ color:#fff; background:var(--stable); }
  .pill.shift{ color:#111; background:#f0d98a; }
  .pill.drift{ color:#fff; background:var(--drift); }
  .big{
    font-size:22px;
    font-weight:800;
    line-height:1.2;
    margin:10px 0 8px;
  }
  .muted{ color:var(--muted); }
  .callout{
    border-left:5px solid #111;
    padding:10px 14px;
    background:#fafbff;
    border-radius:8px;
    margin-top:12px;
    font-size:17px;
  }
  .footer{
    margin-top:18px;
    color:var(--muted);
    font-size:14px;
  }
  @media (max-width: 820px){
    .grid{ grid-template-columns:1fr; }
    h1{ font-size:28px; }
  }
</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <h1>RedLINE Timing Drift Demo</h1>
    <div class="sub">A dead-simple proof of concept: the event has not happened yet, but the spacing between actions is already stretching. That timing change is the early signal.</div>
  </div>

  <div class="grid">
    <div class="card">
      <div class="controls">
        <button class="primary" id="runBtn">Run Demo</button>
        <button class="secondary" id="resetBtn">Reset</button>
      </div>
      <div class="legend">
        <span><span class="dot stable"></span>Stable cadence</span>
        <span><span class="dot shift"></span>Early shift</span>
        <span><span class="dot drift"></span>Drift forming</span>
      </div>
      <div class="timeline" id="timeline">
        <div class="axis"></div>
      </div>
      <div class="callout" id="callout">
        Start the demo. Watch the spacing stretch before anything “fails.”
      </div>
    </div>

    <div class="card">
      <div class="miniTitle">What this proves</div>
      <div class="big">Timing shifts upstream. Problems show up downstream.</div>
      <div class="muted">This is not a finished product demo. It is proof of the behavior RedLINE is built around.</div>

      <div class="miniTitle" style="margin-top:16px;">Event spacing</div>
      <table id="intervalTable">
        <thead>
          <tr>
            <th>#</th>
            <th>Time</th>
            <th>Gap</th>
            <th>State</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>

      <div class="miniTitle" style="margin-top:16px;">How to say it in the meeting</div>
      <div class="muted">“I’m not claiming a finished system here. I’m showing that spacing changes before a visible event — and that this change can be seen.”</div>
    </div>
  </div>

  <div class="footer">Tip: open this in Safari or Chrome and click <b>Run Demo</b>. It is self-contained and works offline.</div>
</div>

<script>
const events = [
  {t:0, gap:"—", state:"stable"},
  {t:5, gap:"5", state:"stable"},
  {t:10, gap:"5", state:"stable"},
  {t:15, gap:"5", state:"stable"},
  {t:21, gap:"6", state:"shift"},
  {t:28, gap:"7", state:"shift"},
  {t:36, gap:"8", state:"drift"},
  {t:45, gap:"9", state:"drift"}
];

const timeline = document.getElementById("timeline");
const tbody = document.querySelector("#intervalTable tbody");
const callout = document.getElementById("callout");
const runBtn = document.getElementById("runBtn");
const resetBtn = document.getElementById("resetBtn");

let timers = [];

function clearTimers(){
  timers.forEach(t => clearTimeout(t));
  timers = [];
}

function renderBands(){
  document.querySelectorAll(".phaseBand").forEach(n => n.remove());
  const maxT = events[events.length - 1].t;
  const left = 54;
  const width = timeline.clientWidth - 74;

  const bands = [
    {start:0, end:15, text:"Stable", color:"rgba(31,122,31,.12)"},
    {start:15, end:28, text:"Shift begins", color:"rgba(184,134,11,.18)"},
    {start:28, end:45, text:"Drift forming", color:"rgba(178,34,34,.12)"}
  ];

  bands.forEach(b => {
    const div = document.createElement("div");
    div.className = "phaseBand";
    const x1 = left + (b.start/maxT)*width;
    const x2 = left + (b.end/maxT)*width;
    div.style.left = x1 + "px";
    div.style.width = Math.max(72, x2 - x1 - 4) + "px";
    div.style.background = b.color;
    div.textContent = b.text;
    timeline.appendChild(div);
  });
}

function resetDemo(){
  clearTimers();
  document.querySelectorAll(".event,.label,.phaseBand").forEach(n => n.remove());
  tbody.innerHTML = "";
  renderBands();
  callout.textContent = "Start the demo. Watch the spacing stretch before anything “fails.”";
}

function eventColor(state){
  if(state === "stable") return "var(--stable)";
  if(state === "shift") return "var(--shift)";
  return "var(--drift)";
}

function pill(state){
  return '<span class="pill ' + state + '">' + state + '</span>';
}

function addEvent(index){
  const e = events[index];
  const maxT = events[events.length - 1].t;
  const left = 54;
  const width = timeline.clientWidth - 74;
  const x = left + (e.t/maxT)*width;

  const dot = document.createElement("div");
  dot.className = "event";
  dot.style.left = x + "px";
  dot.style.background = eventColor(e.state);
  timeline.appendChild(dot);

  const label = document.createElement("div");
  label.className = "label";
  label.style.left = x + "px";
  label.textContent = e.t + " min";
  timeline.appendChild(label);

  const tr = document.createElement("tr");
  tr.innerHTML = `<td>${index + 1}</td><td>${e.t} min</td><td>${e.gap} min</td><td>${pill(e.state)}</td>`;
  tbody.appendChild(tr);

  if(index < 4){
    callout.textContent = "Cadence is stable. Nothing looks wrong.";
  } else if(index < 6){
    callout.textContent = "The event still has not happened — but spacing is already stretching.";
  } else {
    callout.textContent = "Drift is forming. This is the early-warning window before visible failure.";
  }
}

function runDemo(){
  resetDemo();
  let elapsed = 0;
  events.forEach((e, i) => {
    const delay = i === 0 ? 350 : 700;
    elapsed += delay;
    const timer = setTimeout(() => addEvent(i), elapsed);
    timers.push(timer);
  });
}

window.addEventListener("resize", resetDemo);
runBtn.addEventListener("click", runDemo);
resetBtn.addEventListener("click", resetDemo);
resetDemo();
</script>
</body>
</html>
