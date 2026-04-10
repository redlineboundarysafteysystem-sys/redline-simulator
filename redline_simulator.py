import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="RedLINE Simulator", layout="wide")
st.title("RedLINE — Upstream Timing Deviation Detector")
st.markdown("**Environmental Boundary and Timing Deviation Detection System** (Provisional Patent Pending)")

# Sidebar for input
st.sidebar.header("Input Event Stream")
option = st.sidebar.radio("Data source", ["Paste timestamps (one per line)", "Upload CSV"])

if option == "Paste timestamps (one per line)":
    timestamps_str = st.sidebar.text_area("Enter timestamps (e.g., 2026-04-09 10:00:00)", 
        value="2026-04-09 10:00:00\n2026-04-09 10:05:00\n2026-04-09 10:10:00\n2026-04-09 10:15:00\n2026-04-09 10:21:00\n2026-04-09 10:28:00\n2026-04-09 10:36:00\n2026-04-09 10:45:00")
    times = [datetime.fromisoformat(ts.strip()) for ts in timestamps_str.strip().split("\n") if ts.strip()]
else:
    uploaded = st.sidebar.file_uploader("Upload CSV with 'timestamp' column", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        times = pd.to_datetime(df['timestamp']).tolist()

if 'times' in locals() and len(times) > 1:
    # Compute intervals in minutes
    intervals = [(times[i+1] - times[i]).total_seconds() / 60 for i in range(len(times)-1)]
    df = pd.DataFrame({
        'Event': range(1, len(times)+1),
        'Timestamp': times,
        'Gap_min': [np.nan] + intervals
    })
    
    # Simple RedLINE classification (customize these thresholds)
    baseline = np.mean(intervals[:3]) if len(intervals) > 3 else np.mean(intervals)  # early stable window
    tolerance_shift = 1.25  # 25% stretch = shifting
    tolerance_drift = 1.6   # 60%+ = drifting
    
    states = []
    for gap in intervals:
        if gap <= baseline * tolerance_shift:
            states.append("Stable")
        elif gap <= baseline * tolerance_drift:
            states.append("Shifting")
        else:
            states.append("Drifting")
    
    df['State'] = ["-"] + states
    df['Color'] = df['State'].map({"Stable": "green", "Shifting": "orange", "Drifting": "red", "-": "gray"})
    
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
    timestamps_str = st.sidebar.text_area("Enter timestamps (YYYY-MM-DD HH:MM:SS, one per line)", 
        value="2026-04-09 10:00:00\n2026-04-09 10:05:00\n2026-04-09 10:10:00\n2026-04-09 10:15:00\n2026-04-09 10:21:00\n2026-04-09 10:28:00\n2026-04-09 10:36:00\n2026-04-09 10:45:00")
    times = []
    for ts in timestamps_str.strip().split("\n"):
        if ts.strip():
            try:
                times.append(datetime.fromisoformat(ts.strip()))
            except:
                st.sidebar.error(f"Invalid timestamp: {ts}")
else:
    uploaded = st.sidebar.file_uploader("Upload CSV with 'timestamp' column", type="csv")
    if uploaded:
        df = pd.read_csv(uploaded)
        times = pd.to_datetime(df['timestamp']).tolist()

if len(times) > 1:
    # Compute intervals in minutes
    intervals = [(times[i+1] - times[i]).total_seconds() / 60 for i in range(len(times)-1)]
    
    df = pd.DataFrame({
        'Event': range(1, len(times)+1),
        'Timestamp': times,
        'Gap_min': [np.nan] + intervals
    })
    
    # RedLINE classification
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
    df['Color'] = df['State'].map({"Stable": "green", "Shifting": "orange", "Drifting": "red", "-": "gray"})
    
    # Main layout
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
            st.success("Cadence is stable. The spacing is consistent. Nothing looks wrong yet.")
        elif last_state == "Shifting":
            st.warning("The spacing is beginning to stretch. This is the early shift. Visible failure still ahead.")
        else:
            st.error("Drift is forming before visible failure. This is the upstream window RedLINE reveals.")
    
    with col2:
        st.subheader("Observed Intervals")
        st.dataframe(df[['Event', 'Timestamp', 'Gap_min', 'State']], use_container_width=True)
        
        st.subheader("Bottom Line")
        st.info("Timing shifts appear **upstream**. RedLINE flags the change before downstream breakage.")
        
        st.caption("This is a lightweight simulator of the RedLINE framework. Provisional Patent Pending.")
else:
    st.info("Paste at least 2 timestamps in the sidebar to see the RedLINE analysis.")
