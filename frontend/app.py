import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px

# Configuration
API_URL = "http://127.0.0.1:8000"
st.set_page_config(layout="wide", page_title="AEGIS | PROJECT X", initial_sidebar_state="collapsed")

# Custom CSS for Cyberpunk UI
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Share Tech Mono', monospace;
    background-color: #050505;
    color: #00fbfb;
}

/* Background grid effect */
.stApp {
    background-image: 
        linear-gradient(rgba(0, 251, 251, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 251, 251, 0.05) 1px, transparent 1px);
    background-size: 20px 20px;
    background-position: center center;
}

/* Scanline effect */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
    background-size: 100% 2px, 3px 100%;
    z-index: 9999;
    pointer-events: none;
    opacity: 0.3;
}

h1, h2, h3, h4, h5, h6 {
    color: #00fbfb !important;
    text-shadow: 0 0 10px #00fbfb;
}

/* Headers */
.cyber-header {
    border-bottom: 2px solid #00fbfb;
    padding-bottom: 5px;
    margin-bottom: 15px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* Containers with glow */
div[data-testid="stVerticalBlock"] > div > div {
    /* Use selective application if needed */
}

/* Panels */
.cyber-panel {
    border: 1px solid #00fbfb;
    box-shadow: 0 0 10px rgba(0, 251, 251, 0.2);
    padding: 15px;
    background: rgba(5, 5, 5, 0.8);
    border-radius: 4px;
    margin-bottom: 15px;
}

.terminal-text {
    color: #00fbfb;
    font-size: 14px;
    text-shadow: 0 0 2px #00fbfb;
}

.terminal-error {
    color: #e00460;
    font-size: 14px;
    text-shadow: 0 0 5px #e00460;
}

.terminal-cursor {
    display: inline-block;
    width: 10px;
    height: 15px;
    background-color: #00fbfb;
    animation: blink 1s step-end infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

/* Button style */
button[kind="primary"] {
    background-color: transparent !important;
    color: #00fbfb !important;
    border: 1px solid #00fbfb !important;
    box-shadow: 0 0 10px #00fbfb !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    transition: all 0.3s ease;
}

button[kind="primary"]:hover {
    background-color: rgba(0, 251, 251, 0.2) !important;
    color: #fff !important;
    border-color: #fff !important;
}

/* ASCII Title */
.ascii-title {
    color: #e00460;
    white-space: pre;
    font-size: 12px;
    text-shadow: 0 0 10px #e00460;
    line-height: 1.2;
    margin-bottom: 20px;
}

/* Metric styling */
label[data-testid="stWidgetLabel"] {
    color: #00fbfb !important;
}
div[data-testid="stMetricValue"] {
    color: #fff !important;
    text-shadow: 0 0 10px #00fbfb;
}

</style>
"""

st.markdown(css, unsafe_allow_html=True)

# Data Fetching
@st.cache_data(ttl=5)
def fetch_data(endpoint):
    try:
        r = requests.get(f"{API_URL}/{endpoint}", timeout=2)
        r.raise_for_status()
        return r.json(), False
    except Exception as e:
        return None, True

def get_sys_status(is_offline):
    if is_offline:
        return "<span style='color:#e00460; text-shadow: 0 0 5px #e00460;'>OFFLINE</span>"
    return "<span style='color:#00fbfb; text-shadow: 0 0 5px #00fbfb;'>OK</span>"

# Data loading
nodes, nodes_offline = fetch_data("nodes")
heatmap, heatmap_offline = fetch_data("heatmap")
events, events_offline = fetch_data("events?limit=20")
assets, assets_offline = fetch_data("assets")

is_offline = nodes_offline

# Fallback mocked data if offline
if is_offline:
    nodes = [{"node_id": "MOCK-01", "risk_score": 0.8, "flags": ["ddos", "error"], "is_online": True, "last_latency": 250},
             {"node_id": "MOCK-02", "risk_score": 0.1, "flags": [], "is_online": True, "last_latency": 15}]
    events = [{"timestamp": "2026-03-25T12:00:00", "node_id": "MOCK-01", "flags": ["error", "ddos"], "status_code": 500, "latency": 250}]
    heatmap = [{"node_id": "MOCK-01", "time": "2026-03-25T12:00:00", "latency": 250}]
    assets = [{"node_id": "MOCK-01", "serial": "SN-MOCK"}]

# UI Layout
# Top Bar
st.markdown(f"""
<div style='display: flex; justify-content: space-between; border-bottom: 1px solid #00fbfb; padding-bottom: 10px; margin-bottom: 20px;'>
    <div style='font-weight: bold;'>&gt;NEURAL_OS_v8.4</div>
    <div style='font-size: 0.9em;'>STATUS: {get_sys_status(is_offline)} &nbsp;&nbsp;|&nbsp;&nbsp; NETWORK: CONNECTED</div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([0.7, 0.3])

with col_left:
    st.markdown("<div class='cyber-header'>&gt; TERMINAL_CONSOLE</div>", unsafe_allow_html=True)
    
    # ASCII Art
    ascii_art = r"""
    ____  _____  ___    _  ____  ____    __  __
   / __ \/  _/ |/ / |  / // __ \/ __/   / / / /
  / /_/ // //    /| | / // / / /\ \    / /_/ / 
 / ____// // /| / | |/ // /_/ /___/   / __  /  
/_/   /___/_/ |_| |___/ \____//____/  /_/ /_/  
                                               
    """
    st.markdown(f"<div class='ascii-title'>{ascii_art}</div>", unsafe_allow_html=True)
    
    st.progress(0.85, text="SYSTEM BOOT SEQUENCE... 85%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Terminal Stream
    term_html = "<div class='cyber-panel' style='height: 300px; overflow-y: auto;'>"
    if events:
        for ev in reversed(events):
            status_code_val = int(ev.get("status_code", 200))
            color_class = "terminal-error" if "error" in ev.get("flags", []) or status_code_val >= 500 else "terminal-text"
            flags_list = ev.get("flags", [])
            flags_str = f" [{','.join([str(x) for x in flags_list])}]" if flags_list else ""
            term_html += f"<div class='{color_class}'>[{ev.get('timestamp', '')}] SYS_LOG: Node {ev.get('node_id', '')} responded with {status_code_val} (Lat: {float(ev.get('latency', 0)):.2f}ms){flags_str}</div>"
    else:
        term_html += "<div class='terminal-text'>Waiting for data stream...</div>"
    
    # Blinking cursor
    term_html += "<div><span class='terminal-text'>root@aegis:~# </span><span class='terminal-cursor'></span></div>"
    term_html += "</div>"
    
    st.markdown(term_html, unsafe_allow_html=True)
    
    # Button
    if st.button("LAUNCH OVERRIDE", type="primary"):
        st.toast("OVERRIDE INITIATED")
        
    st.markdown("<br><div class='cyber-header'>&gt; DATA VISUALIZATION</div>", unsafe_allow_html=True)
    
    # Heatmap
    if heatmap:
        df_hm = pd.DataFrame(heatmap)
        if not df_hm.empty:
            df_hm['time'] = pd.to_datetime(df_hm['time'])
            fig = px.scatter(df_hm, x='time', y='latency', color='node_id', 
                             title="Latency Heatmap",
                             color_discrete_sequence=px.colors.qualitative.Set1)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#00fbfb', family="Share Tech Mono"),
                xaxis=dict(showgrid=True, gridcolor='rgba(0,251,251,0.1)', title="Timeline"),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,251,251,0.1)', title="Latency (ms)"),
                margin=dict(l=0, r=0, t=30, b=0)
            )
            # Custom trace styling
            fig.update_traces(marker=dict(size=6, opacity=0.8, line=dict(width=1, color='#00fbfb')))
            st.plotly_chart(fig, use_container_width=True)
            
    # Node Risk Map
    st.markdown("<div style='margin-top:20px;' class='terminal-text'>NODE RISK GRID</div>", unsafe_allow_html=True)
    if nodes:
        df_nodes = pd.DataFrame(nodes)
        df_nodes['risk_score'] = df_nodes['risk_score'].round(2)
        st.dataframe(df_nodes[['node_id', 'risk_score', 'last_latency', 'flags']], use_container_width=True, hide_index=True)

with col_right:
    # 1. EVENTS
    st.markdown("<div class='cyber-header'>&gt;EVENTS</div>", unsafe_allow_html=True)
    html_ev = "<div class='cyber-panel' style='min-height: 200px;'>"
    anomalies = [e for e in events if e.get("flags")] if events else []
    if anomalies:
        for a in anomalies[:5]:
            flags = ",".join(a["flags"])
            html_ev += f"<div style='margin-bottom:10px;'><span style='color:#e00460; font-weight:bold;'>[!] {flags.upper()}</span><br><span style='font-size:12px; color:#aaa;'>Node: {a['node_id']} | Latency: {a.get('latency',0):.1f}ms</span></div>"
    else:
        html_ev += "<div class='terminal-text' style='color:#00fbfb; opacity:0.7;'>No active anomalies. System normal.</div>"
    html_ev += "</div>"
    st.markdown(html_ev, unsafe_allow_html=True)
    
    st.progress(0.42, text="THREAT LEVEL: 42%")
    
    # 2. SETTINGS
    st.markdown("<div class='cyber-header' style='margin-top:20px;'>&gt;SETTINGS</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='cyber-panel terminal-text'>
        MOD_STATE: <span style='color:#00fbfb; font-weight:bold;'>ACTIVE</span><br>
        THEME_PROFILE: <span style='color:#e00460; text-shadow:0 0 5px #e00460;'>CYBERPUNK</span><br>
        AUTO-REFRESH: <span style='color:#00fbfb;'>ENABLED</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 3. WHOAMI
    st.markdown("<div class='cyber-header' style='margin-top:20px;'>&gt;WHOAMI</div>", unsafe_allow_html=True)
    total_nodes = len(nodes) if nodes else 0
    active_assets = len(assets) if assets else 0
    st.markdown(f"""
    <div class='cyber-panel terminal-text'>
        USER: ROOT<br>
        IP: 192.168.0.UNKNOWN<br>
        NODES MONITORED: {total_nodes}<br>
        ASSETS DECODED: {active_assets}
    </div>
    """, unsafe_allow_html=True)

# Auto refresh trick
time.sleep(3)
st.rerun()
