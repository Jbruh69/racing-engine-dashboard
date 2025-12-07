import streamlit as st
import pandas as pd
from io import StringIO

# ═══════════════════════════════════════════════════════════════════════════════
# EMBEDDED ENGINE DATA
# ═══════════════════════════════════════════════════════════════════════════════

ENGINE_DATA = """Car,Engine,Engine Weight (KG),Proto Weight No Turbo,Low Torque(Nm),Medium Torque(Nm),High Torque(Nm),Rev Limiter,Turbo,Peak RPM,HorsePower,Turbine Pressure,Class
HC6,DA15,140,,109,107,110,7800,No,8000,122,,C1
NX5,PF1,155,,126,130,126,7200,No,7500,127,,C1
DTS,DL20,160,,187,168,144,6200,No,6500,138,,C1
NX5C,PF1,155,,131,134,130,7200,No,7500,131,,C1
PF7,PV8,270,,285,305,232,5000,No,5300,203,,C1
ECL,G64,185,,214,213,188,6500,No,6800,174,,C1
E86,GE4,154,,121,135,128,7400,No,7600,132,,C1
2MR,GE3,143,,165,169,165,7000,No,7300,163,,C1
B19,ME10,170,127kg,196,223,189,6600,No,7500,165,,C1
FLD,30S,249,,164,159,158,7000,No,7300,151,,C1
M36,B28,180,,257,245,207,6600,No,6900,193,,C1
20R,S02,199,,179,170,156,7300,No,7700,160,,C1
30Z,VGD3,220,159kg,158,164,149,6800,Yes,7100,221,0.62,C1
S18,DT18,268,,143,153,114,7200,Yes,7500,185,0.6,C1
V7G,2TS,140,,187,186,144,6000,Yes,6300,201,0.55,C1
G86,GU4,200,,193,204,193,7400,No,7700,198,,C1
MCS,N14B,130,99kg,156,136,118,6500,Yes,6700,172,0.55,C1
SFR,E25,120,90kg,189,171,137,6500,Yes,6800,225,0.79,C1
L08,L08,127,93kg,119,125,93,6000,No,6300,93,,C1
VAN,M3G6,199,,484,375,325,4800,No,5200,245,,C1
V45,B1A6,140,107kg,126,140,136,6500,No,7000,119,,C1
FX7,B13,157,,78,85,86,8500,Yes,8800,197,0.75,C2
Z31,V30G,178,,251,219,203,6000,Yes,6300,228,0.34,C2
M46,SB53,149,,251,274,256,7000,No,7300,244,,C2
CHR,BV8,281,234,449,386,319,6400,No,6600,293,,C2
32R,DT20,230,,183,182,124,7400,Yes,7700,233,0.7,C2
R86,GU4,171,,253,303,209,7200,No,7700,235,,C2
FST,RDA,109,,241,210,175,6500,Yes,6800,249,0.6,C2
CRN,FUZ1,195,,274,338,288,7200,No,7500,280,,C2
M30,S1B4,136,,185,203,207,6750,No,7050,197,,C2
WRS,E25,125,,247,265,131,7400,Yes,7700,272,0.7,C2
S14,RS20T,180,,128,161,139,7500,Yes,7800,220,0.65,C2
HC9,B1B6,184,,147,156,162,8500,No,8000,185,,C2
HCR,KA20,145,118,337,320,270,8100,No,8300,260,,C2
TTR,TF25,160,,140,140,127,6800,Yes,7000,280,1.35,C2
S13,RS20T,180,,140,167,145,7500,Yes,7800,205,0.48,C2
S15,RS20T,180,,173,186,160,7500,Yes,7800,229,0.6,C2
S80,JAZ22,230,,187,228,198,7000,Yes,7300,276,0.6,C2
P64,MT64,150,,190,206,165,7100,Yes,7500,272,0.8,C2
DC2,HEM5,254,,527,518,371,5800,No,6100,370,,C2
HI5,KA20,180,,188,191,205,8000,No,8000,220,,C2
Z35,QD35,205,,314,333,311,6800,No,7100,288,,C2
Z37,QH37,174,,321,338,308,6800,No,7100,293,,C2
TM2,JAZ11,210,,175,175,169,7000,Yes,7300,286,0.82,C2
CRT,JAZ11,210,,175,175,169,7000,Yes,7300,286,0.82,C2
HS2,F2C0,147,,169,169,201,8300,No,9300,230,,C2
F69,FV8,290,,422,428,332,6200,No,6500,317,,C2
34R,DT25,250,,190,202,195,7000,Yes,7300,301,0.7,C2
EV9,GT63,195,,207,240,190,7500,Yes,7800,275,0.6,C2
EVX,B411T,134,,265,285,226,7800,Yes,7800,296,0.5,C2
WRS,E20J7,204,,226,258,200,8000,Yes,8300,276,0.5,C2
M93,B30,135,,315,284,207,6800,Yes,7100,342,0.65,C2
CMR,LL1,193,,418,464,390,6400,No,6700,354,,C2
M39,M6B244,208,,347,341,299,7000,No,7300,285,,C2
M92C,B30,135,,315,284,207,6800,Yes,7100,342,0.65,C2
63C,DE27,367,,345,373,310,6800,Yes,7100,421,0.6,C3
EV6,4G63,170,,147,129,124,7600,Yes,7800,280,1.1,C3
B31,SB70,155,,480,453,385,6400,No,6800,381,,C3
S90,BL58,140,110,288,301,222,7000,Yes,7200,333,0.75,C3
F35,VF52,195,,380,414,375,7200,No,7450,376,,C3
S65,FC3,186,144,273,274,234,7500,Yes,7800,399,0.82,C3
DX7,BR13,120,,213,213,198,8300,Yes,8500,280,0.41,C3
6RS,CV6,190,,342,353,322,6700,Yes,7000,436,0.6,C3
STR,ES8,245,,498,509,399,7250,No,7500,427,,C3
M4R,B58,140,113,285,286,242,7000,Yes,7300,357,0.75,C3
B60,85S,240,,256,303,350,8250,No,8550,411,,C3
HSS,SCHM,240,,448,512,477,6500,No,6700,431,,C3
BM2,B55N,194,,171,192,188,7500,Yes,7800,371,1.16,C3
M90,S6B34T,229,,227,233,237,8250,Yes,8500,454,1.5,C3
35R,RV38,276,,293,326,281,7500,Yes,7700,409,0.75,C3
P91,97M1,230,,211,232,187,7300,Yes,8800,355,1,C3
HSX,BC32,200,,279,276,276,8000,No,8250,295,,C3
C70,GCTM1,242,,392,431,375,7500,No,7800,360,,C3
CC6,SS2,201,,456,462,375,7000,No,7250,392,,C3
CC7,LL4,267,,517,565,479,6400,No,6700,429,,C3
VP1,VV53,230,,447,514,427,6300,No,6600,381,,C3
M4G,S58,160,,173,173,172,6800,Yes,7500,415,1.7,C3
MGTC,MDA,209,,212,212,191,7000,Yes,6700,384,1.35,C3
MGT,MDA,209,,217,217,195,7000,Yes,6700,391,,C3
BX5,S6B34 ,229,,304,304,303,7200,Yes,7500,560,1.37,C3
AR8,CPTAV10,250,,172,188,180,7800,Yes,8800,416,1.35,C3
LFL,L1R,160,,290,337,345,9000,No,9300,401,,C3
LMD,LMV12,232,,353,417,393,7300,No,8800,400,,C3
LMH,FSP,250,,156,172,169,8000,Yes,8800,401,1.35,C3
AMV,M17,209,,133,180,173,8000,Yes,7300,382,1.35,C3
290C,BB53,140,,288,301,222,7000,Yes,7300,327,0.75,C3
B8I,38B,210,,239,245,238,6500,Yes,6800,331,0.65,C3
Z40,RV30,240,,265,266,236,6800,Yes,7700,400,1.03,C3
GLW,15M7,220,,356,353,346,6500,Yes,6800,544,1,C3
FGT,EBT,205,,260,287,298,7000,Yes,6800,413,0.6,C4
MLN,M4T,170,,186,185,180,8500,Yes,8800,442,1.3,C4
LMA,53L,235,,427,515,478,8500,No,8800,514,,C4
PGT,M275A,230,,184,191,189,9000,Yes,9300,419,1,C4
DX8*,BM13*,120,,246,243,223,8300,No,8500,247,,C2
IF6*,RV30*,195,148,312,311,305,6800,Yes,7100,400,0.5,C3
33R*,BR26*,280,,165,263,206,7800,Yes,8000,296,0.6,C2
No Car,R20,190,,171,176,160,7200,No,7400,150,,
M34,BS38,150,,214,247,333,6900,No,7300,340,,
VPR,VV53,323,,446,464,514,6200,No,6500,454,,
HNG,R41Y,220,,660,667,658,8000,No,8300,720,,
7RS*,E82A*,190,,373,387,348,6700,Yes,7000,468,0.6,C3
BZ4,BS38*,220,,304,323,311,8000,No,8300,344,,C3
CVL*,LL6S*,270,,530,541,486,6200,No,6500,421,,C3
YRS*,G1E6*,120,,142,143,136,7200,Yes,7600,270,1,C3
HRD*,FC3*,195,,243,293,287,7200,Yes,7500,418,0.7,C3"""

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG & CUSTOM CSS
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Racing Engine Dashboard",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for racing aesthetic
st.markdown("""
<style>
    /* Import racing-inspired fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Header styling */
    .main-header {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #ff6b35, #f7931e, #ffcc00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 40px rgba(255, 107, 53, 0.5);
        margin-bottom: 0.5rem;
        letter-spacing: 3px;
    }
    
    .sub-header {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        text-align: center;
        color: #8892b0;
        margin-bottom: 2rem;
        letter-spacing: 5px;
        text-transform: uppercase;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%);
        border-right: 1px solid #ff6b35;
    }
    
    [data-testid="stSidebar"] .stMarkdown h2 {
        font-family: 'Orbitron', monospace;
        color: #ff6b35;
        font-size: 1.2rem;
        border-bottom: 2px solid #ff6b35;
        padding-bottom: 10px;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #1a1a2e, #0f0f23);
        border: 1px solid #ff6b35;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 20px rgba(255, 107, 53, 0.2);
    }
    
    [data-testid="stMetric"] label {
        font-family: 'Rajdhani', sans-serif;
        color: #8892b0 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-family: 'Orbitron', monospace;
        color: #ffffff !important;
        font-size: 1.8rem !important;
    }
    
    /* Engine cards */
    .engine-card {
        background: linear-gradient(145deg, #1a1a2e, #0f0f23);
        border: 1px solid #2a2a4a;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .engine-card:hover {
        border-color: #ff6b35;
        box-shadow: 0 0 30px rgba(255, 107, 53, 0.3);
        transform: translateY(-2px);
    }
    
    .engine-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #ff6b35, #f7931e);
    }
    
    .engine-name {
        font-family: 'Orbitron', monospace;
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 5px;
    }
    
    .engine-car {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        color: #8892b0;
        margin-bottom: 15px;
    }
    
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 10px;
    }
    
    .stat-box {
        background: rgba(255, 107, 53, 0.1);
        border: 1px solid #2a2a4a;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
    }
    
    .stat-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.75rem;
        color: #8892b0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stat-value {
        font-family: 'Orbitron', monospace;
        font-size: 1.1rem;
        color: #ffffff;
        font-weight: 600;
    }
    
    /* Rank badges */
    .rank-gold { color: #ffd700; text-shadow: 0 0 10px #ffd700; }
    .rank-silver { color: #c0c0c0; text-shadow: 0 0 10px #c0c0c0; }
    .rank-bronze { color: #cd7f32; text-shadow: 0 0 10px #cd7f32; }
    .rank-normal { color: #ff6b35; }
    
    /* Turbo badge */
    .turbo-badge {
        display: inline-block;
        background: linear-gradient(90deg, #ff6b35, #f7931e);
        color: #000;
        font-family: 'Orbitron', monospace;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        margin-left: 10px;
        letter-spacing: 1px;
    }
    
    /* Class badge */
    .class-badge {
        display: inline-block;
        background: rgba(255, 107, 53, 0.2);
        border: 1px solid #ff6b35;
        color: #ff6b35;
        font-family: 'Orbitron', monospace;
        font-size: 0.7rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 4px;
        margin-left: 10px;
    }
    
    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #ff6b35, transparent);
        margin: 30px 0;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Multiselect styling */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #ff6b35 !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Text input */
    .stTextInput input {
        font-family: 'Rajdhani', sans-serif;
        background: #0f0f23 !important;
        border: 1px solid #2a2a4a !important;
        color: #ffffff !important;
    }
    
    .stTextInput input:focus {
        border-color: #ff6b35 !important;
        box-shadow: 0 0 10px rgba(255, 107, 53, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DATA PROCESSING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_turbo_torque(row):
    """Calculate actual torque for turbocharged engines.
    Formula: Actual torque = base torque + (base torque × turbine pressure)
    """
    low = row.get('Low Torque(Nm)', 0)
    med = row.get('Medium Torque(Nm)', 0)
    high = row.get('High Torque(Nm)', 0)
    
    is_turbo = str(row.get('Turbo', '')).lower() == 'yes'
    pressure = row.get('Turbine Pressure', 0)
    if pd.isna(pressure):
        pressure = 0
    
    if is_turbo and pressure > 0:
        low = low + (low * pressure)
        med = med + (med * pressure)
        high = high + (high * pressure)
    
    return max(low, med, high)


def process_data(df):
    """Process the dataframe and calculate derived metrics."""
    df['Max Torque'] = df.apply(calculate_turbo_torque, axis=1)
    df['Torque to Weight'] = df['Max Torque'] / df['Engine Weight (KG)']
    df['Power to Weight'] = df['HorsePower'] / df['Engine Weight (KG)']
    df['Is Turbo'] = df['Turbo'].str.lower() == 'yes'
    df['Max Torque'] = df['Max Torque'].round(2)
    df['Torque to Weight'] = df['Torque to Weight'].round(3)
    df['Power to Weight'] = df['Power to Weight'].round(3)
    return df


def load_data():
    """Load and process the embedded engine data."""
    df = pd.read_csv(StringIO(ENGINE_DATA))
    return process_data(df)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

# Header
st.markdown('<h1 class="main-header">🏎️ RACING ENGINE DASHBOARD</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Performance Analytics & Comparison Tool</p>', unsafe_allow_html=True)

# Load data
df = load_data()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────────────────────────

st.sidebar.markdown("## 🎛️ FILTERS")

# Search
search = st.sidebar.text_input("🔍 Search Engine or Car", "", placeholder="Type to search...")

# Class filter
all_classes = sorted([str(c) for c in df['Class'].dropna().unique()])
selected_classes = st.sidebar.multiselect(
    "📊 Classes",
    all_classes,
    default=all_classes,
    help="Filter by vehicle class"
)

# Turbo filter
turbo_filter = st.sidebar.radio(
    "⚡ Turbo Type",
    ["All Engines", "Turbo Only", "NA Only"],
    help="Filter by aspiration type"
)

# Sort options
sort_options = {
    "Torque to Weight": "Best T/W Ratio",
    "Max Torque": "Highest Torque",
    "HorsePower": "Most Horsepower",
    "Power to Weight": "Best P/W Ratio",
    "Engine Weight (KG)": "Lightest First"
}
sort_by = st.sidebar.selectbox(
    "📈 Sort By",
    list(sort_options.keys()),
    format_func=lambda x: sort_options[x]
)

# ─────────────────────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────────────────────

filtered = df.copy()

# Search filter
if search:
    search_lower = search.lower()
    filtered = filtered[
        filtered['Engine'].str.lower().str.contains(search_lower, na=False) |
        filtered['Car'].str.lower().str.contains(search_lower, na=False)
    ]

# Class filter
if selected_classes:
    filtered = filtered[filtered['Class'].isin(selected_classes)]

# Turbo filter
if turbo_filter == "Turbo Only":
    filtered = filtered[filtered['Is Turbo']]
elif turbo_filter == "NA Only":
    filtered = filtered[~filtered['Is Turbo']]

# Sort
ascending = sort_by == "Engine Weight (KG)"
filtered = filtered.sort_values(sort_by, ascending=ascending).reset_index(drop=True)

# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY METRICS
# ─────────────────────────────────────────────────────────────────────────────

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🏎️ Total Engines", len(filtered))
with col2:
    st.metric("⚡ Turbocharged", int(filtered['Is Turbo'].sum()))
with col3:
    st.metric("🌬️ Naturally Aspirated", int((~filtered['Is Turbo']).sum()))
with col4:
    avg_tw = filtered['Torque to Weight'].mean()
    st.metric("📊 Avg T/W Ratio", f"{avg_tw:.2f}" if not pd.isna(avg_tw) else "N/A")
with col5:
    avg_hp = filtered['HorsePower'].mean()
    st.metric("🔥 Avg Horsepower", f"{avg_hp:.0f}" if not pd.isna(avg_hp) else "N/A")

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ENGINE LISTINGS
# ─────────────────────────────────────────────────────────────────────────────

if len(filtered) == 0:
    st.warning("No engines match your current filters. Try adjusting your search criteria.")
else:
    for idx, eng in filtered.iterrows():
        rank = idx + 1
        
        # Rank display
        if rank == 1:
            rank_display = "🥇"
            rank_class = "rank-gold"
        elif rank == 2:
            rank_display = "🥈"
            rank_class = "rank-silver"
        elif rank == 3:
            rank_display = "🥉"
            rank_class = "rank-bronze"
        else:
            rank_display = f"#{rank}"
            rank_class = "rank-normal"
        
        # Turbo info
        turbo_badge = '<span class="turbo-badge">⚡ TURBO</span>' if eng['Is Turbo'] else ''
        
        # Boost info
        turbo_pressure = eng.get('Turbine Pressure', 0)
        if pd.isna(turbo_pressure):
            turbo_pressure = 0
        boost_text = f" • {turbo_pressure:.2f} bar" if eng['Is Turbo'] and turbo_pressure > 0 else ""
        
        # Class badge
        class_val = eng.get('Class', '')
        class_badge = f'<span class="class-badge">{class_val}</span>' if pd.notna(class_val) and class_val else ''
        
        # Build card HTML
        card_html = f'''
        <div class="engine-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="engine-name {rank_class}">{rank_display}</span>
                    <span class="engine-name">{eng['Engine']}</span>
                    {turbo_badge}
                    {class_badge}
                </div>
            </div>
            <div class="engine-car">{eng['Car']}{boost_text}</div>
            <div class="stat-grid">
                <div class="stat-box">
                    <div class="stat-label">T/W Ratio</div>
                    <div class="stat-value">{eng['Torque to Weight']:.2f}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Max Torque</div>
                    <div class="stat-value">{eng['Max Torque']:.0f} Nm</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Weight</div>
                    <div class="stat-value">{eng['Engine Weight (KG)']:.0f} kg</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Horsepower</div>
                    <div class="stat-value">{eng['HorsePower']:.0f} HP</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Peak RPM</div>
                    <div class="stat-value">{int(eng['Peak RPM'])}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Rev Limit</div>
                    <div class="stat-value">{int(eng['Rev Limiter'])}</div>
                </div>
            </div>
        </div>
        '''
        st.markdown(card_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #4a4a6a; font-family: 'Rajdhani', sans-serif; font-size: 0.9rem;">
    <p>⚡ <strong>Turbo Calculation:</strong> Actual Torque = Base Torque + (Base Torque × Turbine Pressure)</p>
    <p style="margin-top: 10px; color: #3a3a5a;">Racing Engine Dashboard • Data embedded from engine spreadsheet</p>
</div>
""", unsafe_allow_html=True)
