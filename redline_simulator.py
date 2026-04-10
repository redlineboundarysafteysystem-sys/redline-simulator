import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="RedLINE Simulator", layout="wide")
st.title("🔴🟠🟢 RedLINE — Upstream Timing Deviation Detector")
st.markdown("**Environmental Boundary and Timing Deviation Detection System** (Provisional Patent Pending)")

# Sidebar for input
st.sidebar.header("Input Event Stream")
option = st.sidebar.radio("Data source", ["Paste timestamps (one per line)", "Upload CSV"])

if option == "Paste timestamps (one per line)":
    timestamps_str = st.sidebar.text_area("Enter timestamps (one per line)", 
        value="2026-04-09 10:00:00\n2026-04-09 10:05:00\n2026-04-09 10:10:00\n2026-04-09 10:15:00\n2026-04-09 10:21:00\n2026-04-09 10:28:00\n2026-04-09 10:36:00\n2026-04-09 10:45:00")
    times = [datetime.fromisoformat(ts.strip()) for ts in timestamps_str.strip().split("\n") if ts.strip()]
else:
    uploaded = st.sidebar.file_uploader("Upload CSV with 'timestamp' column", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        times = pd.to_datetime(df['timestamp']).tolist()

if 'times' in locals() and len(times) > 1:
    # Calculate gaps
    intervals = [(times[i+1] - times[i]).total_seconds() / 60 for i in range(len(times)-1)]
    
    df = pd.DataFrame({
        'Event': range(1, len(times)+1),
        'Timestamp': times,
        'Gap_min': [np.nan] + intervals
    })
    
    # RedLINE logic
    baseline = np.mean(intervals[:4]) if len(intervals) > 4 else np.mean(intervals)
    tolerance_shift = 1.25
    tolerance_drift = 1.60
    
    states = []
    for gap in intervals:
        if gap <= baseline * tolerance_shift:
            states.append("Stable")
        elif gap <= baseline * tolerance_drift:
            states.append("Shifting")
        else:
            states.append("Drifting")
    
    df['State'] = ["-"] + states
    
    # Display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Timing View")
        fig = px.scatter(df, x='Timestamp', y=[1]*len(df), color='State',
                         color_discrete_map={"Stable":"green", "Shifting":"orange", "Drifting":"red"},
                         title="Event Cadence — Watch spacing stretch upstream")
        fig.update_traces(marker=dict(size=12))
        fig.update_layout(yaxis_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**What the room should notice**")
        last_state = states[-1] if states else "Stable"
        if last_state == "Stable":
            st.success("Cadence is stable. Spacing is consistent.")
        elif last_state == "Shifting":
            st.warning("The spacing is beginning to stretch. Early shift detected.")
        else:
            st.error("Drift is forming before visible failure. This is the upstream window RedLINE reveals.")
    
    with col2:
        st.subheader("Observed Intervals")
        st.dataframe(df[['Event', 'Timestamp', 'Gap_min', 'State']], use_container_width=True)
        
        st.subheader("Bottom Line")
        st.info("Timing shifts appear **upstream**. RedLINE flags the change before downstream breakage.")
        
        st.caption("Lightweight simulator of the RedLINE framework • Provisional Patent Pending")
else:
    st.info("Add timestamps in the sidebar to see RedLINE in action.")
