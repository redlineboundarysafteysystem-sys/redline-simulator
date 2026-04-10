import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="RedLINE Simulator", layout="centered")
st.title("🔴🟠🟢 RedLINE — Upstream Timing Deviation Detector")
st.markdown("**Environmental Boundary and Timing Deviation Detection System** (Provisional Patent Pending)")

st.subheader("Paste your timestamps below")

timestamps_str = st.text_area("Enter timestamps (one per line)", height=200, 
    value="2026-04-09 10:00:00\n2026-04-09 10:05:00\n2026-04-09 10:10:00\n2026-04-09 10:15:00\n2026-04-09 10:21:00\n2026-04-09 10:28:00\n2026-04-09 10:36:00\n2026-04-09 10:45:00\n2026-04-09 10:55:00\n2026-04-09 11:10:00\n2026-04-09 11:30:00\n2026-04-09 12:00:00")

if st.button("🚀 Run RedLINE Demo", type="primary"):
    if timestamps_str.strip():
        try:
            times = [datetime.fromisoformat(ts.strip()) for ts in timestamps_str.strip().split("\n") if ts.strip()]
            
            if len(times) < 2:
                st.error("Please enter at least 2 timestamps.")
            else:
                intervals = [(times[i+1] - times[i]).total_seconds() / 60 for i in range(len(times)-1)]
                
                baseline = sum(intervals[:4]) / 4 if len(intervals) > 4 else sum(intervals) / len(intervals)
                
                st.subheader("Results")
                
                for i, (t, gap) in enumerate(zip(times[1:], intervals)):
                    if gap <= baseline * 1.2:
                        color = "🟢 Stable"
                        msg = "Cadence is stable"
                    elif gap <= baseline * 1.8:
                        color = "🟠 Shifting"
                        msg = "The spacing is beginning to stretch"
                    else:
                        color = "🔴 Drifting"
                        msg = "Drift is forming before visible failure"
                    
                    st.write(f"**{color}** — Gap: {gap:.1f} min | {msg}")
                
                st.success("✅ This is the upstream window RedLINE is built to reveal.")
                st.info("Timing shifts appear **upstream**. Visible problems show up downstream.")
                
        except:
            st.error("Please use the format YYYY-MM-DD HH:MM:SS")
    else:
        st.warning("Please enter some timestamps first.")
