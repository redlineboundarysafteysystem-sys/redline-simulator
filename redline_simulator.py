import streamlit as st
from datetime import datetime

st.title("🔴🟠🟢 RedLINE — Upstream Timing Deviation Detector")
st.markdown("**Environmental Boundary and Timing Deviation Detection System** (Provisional Patent Pending)")

st.subheader("Paste your timestamps (one per line)")

timestamps = st.text_area("Timestamps", height=250, 
    value="2026-04-09 10:00:00\n2026-04-09 10:05:00\n2026-04-09 10:10:00\n2026-04-09 10:15:00\n2026-04-09 10:20:00\n2026-04-09 10:30:00\n2026-04-09 10:45:00\n2026-04-09 11:05:00\n2026-04-09 11:30:00\n2026-04-09 12:00:00")

if st.button("🚀 Run RedLINE Demo", type="primary"):
    lines = [line.strip() for line in timestamps.split("\n") if line.strip()]
    if len(lines) < 3:
        st.error("Please enter at least 3 timestamps")
    else:
        try:
            times = [datetime.fromisoformat(line) for line in lines]
            gaps = [(times[i+1] - times[i]).total_seconds() / 60 for i in range(len(times)-1)]
            
            st.subheader("RedLINE Analysis")
            
            baseline = sum(gaps[:3]) / 3
            
            for i, gap in enumerate(gaps):
                if gap <= baseline * 1.25:
                    st.success(f"🟢 Stable — Gap {gap:.1f} min")
                elif gap <= baseline * 2.0:
                    st.warning(f"🟠 Shifting — Gap {gap:.1f} min  ← Early signal")
                else:
                    st.error(f"🔴 Drifting — Gap {gap:.1f} min  ← Upstream deviation detected")
            
            st.info("Timing shifts appear **upstream**. This is the window RedLINE is built to reveal.")
            
        except:
            st.error("Make sure timestamps are in YYYY-MM-DD HH:MM:SS format")
