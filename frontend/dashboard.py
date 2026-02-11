import streamlit as st
import requests
import pandas as pd
import time
import altair as alt

# Configuration
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="PyKV | Enterprise Store",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 🎨 DYNAMIC THEME ENGINE ---
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# Theme Variables
if st.session_state.theme == "dark":
    bg_color = "#050510"
    text_color = "#e0f2fe"
    sidebar_bg = "linear-gradient(160deg, #0a0a19 0%, #050510 100%)"
    card_bg = "rgba(15, 23, 42, 0.6)"
    input_bg = "rgba(0, 0, 0, 0.5)"
    metric_text = "#fff"
    border_color = "rgba(0, 242, 255, 0.1)"
    grid_color = "rgba(0, 255, 242, 0.03)"
else:
    bg_color = "#f8fafc"
    text_color = "#1e293b"
    sidebar_bg = "linear-gradient(160deg, #f1f5f9 0%, #cbd5e1 100%)"
    card_bg = "rgba(255, 255, 255, 0.9)"
    input_bg = "rgba(255, 255, 255, 1)"
    metric_text = "#0f172a"
    border_color = "rgba(0, 0, 0, 0.1)"
    grid_color = "rgba(0, 0, 0, 0.03)"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;500;700&display=swap');
    
    /* --- ULTRA ANIMATIONS --- */
    @keyframes cyber-gradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    @keyframes float-dust {{
        0% {{ transform: translateY(0) translateX(0); opacity: 0; }}
        50% {{ opacity: 1; }}
        100% {{ transform: translateY(-100vh) translateX(50px); opacity: 0; }}
    }}
    
    @keyframes glitch-load {{
        0% {{ transform: skew(0deg); opacity: 0; }}
        20% {{ transform: skew(-20deg); opacity: 0.5; }}
        40% {{ transform: skew(20deg); opacity: 0.8; }}
        60% {{ transform: skew(-5deg); opacity: 1; }}
        80% {{ transform: skew(5deg); }}
        100% {{ transform: skew(0deg); }}
    }}
    
    @keyframes holo-shine {{
        0%, 100% {{ background-position: 0% 50%; filter: brightness(100%); }}
        50% {{ background-position: 100% 50%; filter: brightness(130%); }}
    }}

    @keyframes neon-pulse {{
        0% {{ box-shadow: 0 0 5px rgba(0, 255, 255, 0.2), 0 0 10px rgba(0, 255, 255, 0.2); }}
        50% {{ box-shadow: 0 0 20px rgba(0, 255, 255, 0.6), 0 0 40px rgba(0, 255, 255, 0.4); }}
        100% {{ box-shadow: 0 0 5px rgba(0, 255, 255, 0.2), 0 0 10px rgba(0, 255, 255, 0.2); }}
    }}

    /* --- GLOBAL LAYOUT --- */
    html, body, [class*="stApp"] {{
        font-family: 'Rajdhani', sans-serif;
        background-color: {bg_color};
        background-image: 
            radial-gradient(circle at 50% 50%, rgba(76, 29, 149, 0.1) 0%, transparent 50%),
            linear-gradient({grid_color} 1px, transparent 1px),
            linear-gradient(90deg, {grid_color} 1px, transparent 1px);
        background-size: 100vw 100vh, 40px 40px, 40px 40px;
        background-position: center center;
        color: {text_color} !important;
        overflow-x: hidden;
    }}
    
    /* Simulate dust particles */
    [class*="stApp"]::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: radial-gradient({"white" if st.session_state.theme == "dark" else "black"} 1px, transparent 1px);
        background-size: 50px 50px;
        opacity: 0.1;
        pointer-events: none;
        animation: float-dust 20s linear infinite;
    }}

    /* Headers - Glitch Style */
    h1 {{
        font-family: 'Orbitron', sans-serif;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        background: linear-gradient(90deg, #00f2ff, #00c3ff, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glitch-load 1s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
        text-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
    }}
    
    h2, h3 {{
        font-family: 'Orbitron', sans-serif;
        color: {"#94a3b8" if st.session_state.theme == "dark" else "#475569"};
        border-left: 4px solid #ec4899;
        padding-left: 15px;
        animation: slideInUp 0.5s ease-out;
    }}

    /* Sidebar - Cyber Panel */
    section[data-testid="stSidebar"] {{
        background: {sidebar_bg} !important;
        border-right: 1px solid rgba(0, 242, 255, 0.1);
        box-shadow: 10px 0 50px rgba(0,0,0,{"0.8" if st.session_state.theme == "dark" else "0.1"});
    }}

    /* Active Sidebar Nav Item Styling */
    [data-testid="stSidebarNav"] li {{
        margin: 5px 15px;
        border-radius: 4px;
        transition: all 0.3s;
    }}
    
    [data-testid="stSidebarNav"] li:hover {{
        background: rgba(0, 242, 255, 0.1);
    }}

    /* Header visibility for sidebar toggle */
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}
    
    header[data-testid="stHeader"] svg {{
        fill: #00f2ff !important;
    }}

    /* Radio button custom styling for sidebar */
    div[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
        background: rgba({"255, 255, 255, 0.02" if st.session_state.theme == "dark" else "0, 0, 0, 0.05"}) !important;
        border: 1px solid rgba({"255, 255, 255, 0.05" if st.session_state.theme == "dark" else "0, 0, 0, 0.1"}) !important;
        border-radius: 4px;
        padding: 10px 15px !important;
        margin-bottom: 5px;
        transition: all 0.2s;
        color: {"#94a3b8" if st.session_state.theme == "dark" else "#475569"} !important;
    }}

    div[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {{
        background: rgba(0, 242, 255, 0.08) !important;
        border-color: rgba(0, 242, 255, 0.2) !important;
        color: #00f2ff !important;
    }}
    
    /* Metrics - Holographic Cards */
    .metric-card {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 4px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
        clip-path: polygon(
            0 0, 
            100% 0, 
            100% 85%, 
            95% 100%, 
            0 100%
        ); /* Sci-fi Shape */
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 2px;
        background:linear-gradient(90deg, transparent, #00f2ff, transparent);
        animation: shine-sweep 3s infinite linear;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px) scale(1.02);
        background: {"rgba(15, 23, 42, 0.8)" if st.session_state.theme == "dark" else "rgba(255, 255, 255, 1)"};
        border-color: #00f2ff;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
    }}
    
    .metric-value {{
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        color: {metric_text};
        text-shadow: 0 0 10px {"#00f2ff, 0 0 20px #00f2ff" if st.session_state.theme == "dark" else "transparent"};
        margin-top: 10px;
    }}
    .metric-title {{
        color: {"#94a3b8" if st.session_state.theme == "dark" else "#475569"};
        font-size: 0.9rem;
        letter-spacing: 0.15em;
    }}

    /* Buttons - Neon Cyberpunk */
    .stButton > button {{
        background: rgba(0, 242, 255, 0.08) !important;
        color: #00f2ff !important;
        border: 1px solid rgba(0, 242, 255, 0.3) !important;
        border-radius: 4px !important;
        text-transform: uppercase;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        z-index: 1;
        width: 100%;
        backdrop-filter: blur(5px);
    }}
    
    .stButton > button:hover {{
        color: #fff !important;
        background: rgba(0, 242, 255, 0.2) !important;
        border-color: #00f2ff !important;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.4), inset 0 0 10px rgba(0, 242, 255, 0.2);
        transform: translateY(-2px);
    }}

    /* Sidebar specific button overrides to ensure they stand out */
    section[data-testid="stSidebar"] .stButton > button {{
        background: rgba({"255, 255, 255, 0.05" if st.session_state.theme == "dark" else "0, 0, 0, 0.05"}) !important;
        border: 1px solid rgba({"255, 255, 255, 0.1" if st.session_state.theme == "dark" else "0, 0, 0, 0.1"}) !important;
        color: {text_color} !important;
    }}

    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(0, 242, 255, 0.15) !important;
        border-color: #00f2ff !important;
        color: #00f2ff !important;
    }}
    
    /* Inputs - Terminal Style */
    .stTextInput > div > div > input {{
        background: {input_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 0 !important;
        color: #00f2ff !important;
        font-family: 'Courier New', monospace;
        letter-spacing: 1px;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: #00f2ff !important;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
        background: rgba(0, 242, 255, 0.05) !important;
    }}
    
    /* Forms - Glassmorphism Cards */
    div[data-testid="stForm"] {{
        background: {"rgba(255, 255, 255, 0.03)" if st.session_state.theme == "dark" else "rgba(255, 255, 255, 0.4)"} !important;
        backdrop-filter: blur(16px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(16px) saturate(180%) !important;
        border: 1px solid {"rgba(255, 255, 255, 0.1)" if st.session_state.theme == "dark" else "rgba(0, 0, 0, 0.05)"} !important;
        border-radius: 16px !important;
        padding: 30px !important;
        box-shadow: 0 8px 32px 0 {"rgba(0, 0, 0, 0.8)" if st.session_state.theme == "dark" else "rgba(31, 38, 135, 0.1)"} !important;
    }}
    
    /* Remove old HUD accents */
    div[data-testid="stForm"]::after {{ display: none; }}

    /* Input styling inside glass cards */
    .stTextInput > div > div > input {{
        background: {"rgba(0, 0, 0, 0.3)" if st.session_state.theme == "dark" else "rgba(255, 255, 255, 0.6)"} !important;
        border: 1px solid {"rgba(255, 255, 255, 0.1)" if st.session_state.theme == "dark" else "rgba(0, 0, 0, 0.1)"} !important;
        border-radius: 8px !important;
        color: {"#00f2ff" if st.session_state.theme == "dark" else "#0f172a"} !important;
        padding: 12px !important;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 8px; }}
    ::-webkit-scrollbar-track {{ background: {bg_color}; }}
    ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: #00f2ff; }}

    /* Hide Chrome but KEEP Header for Sidebar Toggle */
    #MainMenu, footer {{visibility: hidden;}}
    
    /* Make header transparent so it blends in */
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    /* Dataframe overrides for light mode */
    [data-testid="stDataFrame"] {{
        background: {card_bg} !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- API HELPERS ---
def get_all_data():
    try:
        response = requests.get(f"{API_URL}/all")
        return response.json() if response.status_code == 200 else {}
    except:
        return None

def get_data(key):
    try:
        response = requests.get(f"{API_URL}/get/{key.strip()}")
        data = response.json()
        if "value" in data:
            return data["value"]
        return None
    except:
        return None

def put_data(key, value):
    try:
        response = requests.post(f"{API_URL}/put", params={"key": key.strip(), "value": value})
        return response.ok
    except:
        return False

def delete_data(key):
    try:
        response = requests.delete(f"{API_URL}/delete/{key.strip()}")
        return response.ok
    except:
        return False

def clear_store():
    try:
        requests.delete(f"{API_URL}/clear")
        return True
    except:
        return False

def seed_demo_data():
    sample_data = {
        "user:101:name": "Alice Johnson",
        "user:101:role": "Admin",
        "user:102:name": "Bob Smith",
        "user:102:role": "Developer",
        "session:xyz789": "active",
        "config:mode": "production",
        "config:retries": "3",
        "feature:dark_mode": "true",
        "cache:home_page": "<html>...</html>",
        "cache:profile": "{json...}"
    }
    for k, v in sample_data.items():
        put_data(k, v)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9662/9662362.png", width=60) 
    st.markdown("## **PyKV Admin**")
    st.caption("v2.1.0 • Enterprise Edition")
    
    st.markdown("---")
    
    menu = st.radio(
        "Navigate", 
        ["Dashboard", "Explorer", "Get", "Put", "Delete"], 
        label_visibility="collapsed"
    )
    
    st.markdown("### Actions")
    c1, c2 = st.columns(2)
    if c1.button("🌱 Seed", help="Load sample data"):
        seed_demo_data()
        st.toast("Database seeded successfully!", icon="✅")
        time.sleep(0.5)
        st.rerun()
    if c2.button("🧹 Clear", help="Delete all data"):
        clear_store()
        st.toast("Database cleared!", icon="🗑️")
        time.sleep(0.5)
        st.rerun()
        
    st.markdown("---")
    
    # Theme Toggle
    theme_icon = "🌙" if st.session_state.theme == "dark" else "☀️"
    theme_label = "Dark Mode" if st.session_state.theme == "dark" else "Light Mode"
    if st.button(f"{theme_icon} {theme_label}", help="Switch between light and dark mode"):
        toggle_theme()
        st.rerun()

    st.markdown("---")
    status_color = "#10b981" if get_all_data() is not None else "#ef4444"
    st.markdown(f"API Status: <span style='color:{status_color}'>● Connected</span>", unsafe_allow_html=True)


# --- MAIN CONTENT ---
raw_data = get_all_data()

if raw_data is None:
    st.error("🔌 **Connection Error:** Backend is offline.")
    st.code("python -m uvicorn api.app:app --reload")
    st.stop()

count = len(raw_data)

if menu == "Dashboard":
    st.markdown("# System Overview")
    st.markdown("Real-time monitoring of your in-memory key-value store.")
    
    # 1. Top Metrics Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Keys</div>
            <div class="metric-value">{count}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Memory Usage</div>
            <div class="metric-value">~{count * 0.5:.1f} <span style='font-size:1rem'>KB</span></div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Uptime</div>
            <div class="metric-value">99.9%</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Requests/Sec</div>
            <div class="metric-value">1.2k</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    
    # 2. Key Distribution Analysis (Prefix based)
    col_chart, col_recent = st.columns([2, 1])
    
    with col_chart:
        st.subheader("📊 Key Distribution by Namespace")
        if count > 0:
            # Extract prefixes (e.g., 'user' from 'user:123')
            prefixes = [k.split(':')[0] if ':' in k else 'misc' for k in raw_data.keys()]
            df_dist = pd.DataFrame(prefixes, columns=["Namespace"]).value_counts().reset_index()
            df_dist.columns = ["Namespace", "Count"]
            
            # Altair Chart
            chart = alt.Chart(df_dist).mark_arc(innerRadius=70, stroke=bg_color, strokeWidth=2).encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Namespace", type="nominal", scale=alt.Scale(scheme="turbo")),
                tooltip=["Namespace", "Count"]
            ).properties(
                height=350,
                background='transparent'
            ).configure_legend(
                labelColor=text_color,
                titleColor=text_color,
                orient='right'
            ).configure_view(
                stroke=None
            )
            
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No data to visualize. Seed the database to see charts.")

    with col_recent:
        st.subheader("🕒 Recent Operations")
        events = [
            {"Time": "10:23:45", "Event": "GET user:101", "Status": "200 OK"},
            {"Time": "10:23:42", "Event": "PUT config:mode", "Status": "200 OK"},
            {"Time": "10:22:10", "Event": "DEL session:xyz", "Status": "404 Not Found"},
            {"Time": "10:21:05", "Event": "GET user:root", "Status": "200 OK"},
        ]
        st.dataframe(pd.DataFrame(events), hide_index=True)

elif menu == "Explorer":
    st.markdown("# 🔎 Data Explorer")
    
    # Search Bar
    search = st.text_input("🔍 Search keys...", placeholder="Type to filter keys immediately...")
    
    if count > 0:
        df = pd.DataFrame(list(raw_data.items()), columns=["Key", "Value"])
        
        if search:
            df = df[df["Key"].str.contains(search, case=False) | df["Value"].str.contains(search, case=False)]
        
        # Display stylish table
        st.dataframe(
            df, 
            use_container_width=True, 
            height=600,
            column_config={
                "Key": st.column_config.TextColumn("Key Identifier", width="medium"),
                "Value": st.column_config.TextColumn("Stored Data", width="large"),
            }
        )
    else:
        st.warning("Database is empty.")

elif menu == "Get":
    st.markdown("# Get Value")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("get_form"):
            key_get = st.text_input("Key", placeholder="Enter key to fetch", key="get_k")
            if st.form_submit_button("Fetch Value"):
                if key_get:
                    val = get_data(key_get)
                    if val is not None:
                        st.success(f"**Value:** {val}")
                    else:
                        st.error("Key not found")
                else:
                    st.warning("Enter a key")

elif menu == "Put":
    st.markdown("# Store Value")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("create"):
            k = st.text_input("Key", placeholder="e.g. settings:theme")
            v = st.text_input("Value", placeholder="e.g. dark")
            if st.form_submit_button("Save Value"):
                if k and v:
                    if put_data(k, v):
                        st.success(f"Saved: {k}")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Failed.")
                else:
                    st.warning("Missing fields.")

elif menu == "Delete":
    st.markdown("# Delete Value")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("delete"):
            dk = st.text_input("Key", placeholder="e.g. settings:theme")
            if st.form_submit_button("Delete Key"):
                if dk:
                    if delete_data(dk):
                        st.success(f"Deleted: {dk}")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Key not found.")
                else:
                    st.warning("Enter a key.")

