import streamlit as st
import pandas as pd
import io

# Page setup
st.set_page_config(page_title="🏁 Racing Engine Dashboard", page_icon="🏁", layout="wide")

# Embedded CSV data
CSV_DATA = """Car,Engine,Engine Weight (KG),Low Torque(Nm),Medium Torque(Nm),High Torque(Nm),Rev Limiter,Turbo,Peak RPM,HorsePower,Turbine Pressure,Class
HC6,DA15,140,109,107,110,7800,No,8000,122,,C1
NX5,PF1,155,126,130,126,7200,No,7500,127,,C1
DTS,DL20,160,187,168,144,6200,No,6500,138,,C1
NX5C,PF1,155,131,134,130,7200,No,7500,131,,C1
PF7,PV8,270,285,305,232,5000,No,5300,203,,C1
ECL,G64,185,214,213,188,6500,No,6800,174,,C1
E86,GE4,154,121,135,128,7400,No,7600,132,,C1
2MR,GE3,143,165,169,165,7000,No,7300,163,,C1
B19,ME10,170,196,223,189,6600,No,7500,165,,C1
FLD,30S,249,164,159,158,7000,No,7300,151,,C1
M36,B28,180,257,245,207,6600,No,6900,193,,C1
20R,S02,199,179,170,156,7300,No,7700,160,,C1
30Z,VGD3,220,158,164,149,6800,Yes,7100,221,0.62,C1
S18,DT18,268,143,153,114,7200,Yes,7500,185,0.6,C1
V7G,2TS,140,187,186,144,6000,Yes,6300,201,0.55,C1
G86,GU4,200,193,204,193,7400,No,7700,198,,C1
MCS,N14B,130,156,136,118,6500,Yes,6700,172,0.55,C1
SFR,E25,120,189,171,137,6500,Yes,6800,225,0.79,C1
L08,L08,127,119,125,93,6000,No,6300,93,,C1
VAN,M3G6,199,484,375,325,4800,No,5200,245,,C1
V45,B1A6,140,126,140,136,6500,No,7000,119,,C1
FX7,B13,157,78,85,86,8500,Yes,8800,197,0.75,C2
Z31,V30G,178,251,219,203,6000,Yes,6300,228,0.34,C2
M46,SB53,149,251,274,256,7000,No,7300,244,,C2
CHR,BV8,281,449,386,319,6400,No,6600,293,,C2
32R,DT20,230,183,182,124,7400,Yes,7700,233,0.7,C2
R86,GU4,171,253,303,209,7200,No,7700,235,,C2
FST,RDA,109,241,210,175,6500,Yes,6800,249,0.6,C2
CRN,FUZ1,195,274,338,288,7200,No,7500,280,,C2
M30,S1B4,136,185,203,207,6750,No,7050,197,,C2
WRS,E25,125,247,265,131,7400,Yes,7700,272,0.7,C2
S14,RS20T,180,128,161,139,7500,Yes,7800,220,0.65,C2
HC9,B1B6,184,147,156,162,8500,No,8000,185,,C2
HCR,KA20,145,337,320,270,8100,No,8300,260,,C2
TTR,TF25,160,140,140,127,6800,Yes,7000,280,1.35,C2
S13,RS20T,180,140,167,145,7500,Yes,7800,205,0.48,C2
S15,RS20T,180,173,186,160,7500,Yes,7800,229,0.6,C2
S80,JAZ22,230,187,228,198,7000,Yes,7300,276,0.6,C2
P64,MT64,150,190,206,165,7100,Yes,7500,272,0.8,C2
DC2,HEM5,254,527,518,371,5800,No,6100,370,,C2
HI5,KA20,180,188,191,205,8000,No,8000,220,,C2
Z35,QD35,205,314,333,311,6800,No,7100,288,,C2
Z37,QH37,174,321,338,308,6800,No,7100,293,,C2
TM2,JAZ11,210,175,175,169,7000,Yes,7300,286,0.82,C2
CRT,JAZ11,210,175,175,169,7000,Yes,7300,286,0.82,C2
HS2,F2C0,147,169,169,201,8300,No,9300,230,,C2
F69,FV8,290,422,428,332,6200,No,6500,317,,C2
34R,DT25,250,190,202,195,7000,Yes,7300,301,0.7,C2
EV9,GT63,195,207,240,190,7500,Yes,7800,275,0.6,C2
EVX,B411T,134,265,285,226,7800,Yes,7800,296,0.5,C2
WRS,E20J7,204,226,258,200,8000,Yes,8300,276,0.5,C2
M93,B30,135,315,284,207,6800,Yes,7100,342,0.65,C2
CMR,LL1,193,418,464,390,6400,No,6700,354,,C2
M39,M6B244,208,347,341,299,7000,No,7300,285,,C2
M92C,B30,135,315,284,207,6800,Yes,7100,342,0.65,C2
63C,DE27,367,345,373,310,6800,Yes,7100,421,0.6,C3
EV6,4G63,170,147,129,124,7600,Yes,7800,280,1.1,C3
B31,SB70,155,480,453,385,6400,No,6800,381,,C3
S90,BL58,140,288,301,222,7000,Yes,7200,333,0.75,C3
F35,VF52,195,380,414,375,7200,No,7450,376,,C3
S65,FC3,186,273,274,234,7500,Yes,7800,399,0.82,C3
DX7,BR13,120,213,213,198,8300,Yes,8500,280,0.41,C3
6RS,CV6,190,342,353,322,6700,Yes,7000,436,0.6,C3
STR,ES8,245,498,509,399,7250,No,7500,427,,C3
M4R,B58,140,285,286,242,7000,Yes,7300,357,0.75,C3
B60,85S,240,256,303,350,8250,No,8550,411,,C3
HSS,SCHM,240,448,512,477,6500,No,6700,431,,C3
BM2,B55N,194,171,192,188,7500,Yes,7800,371,1.16,C3
M90,S6B34T,229,227,233,237,8250,Yes,8500,454,1.5,C3
35R,RV38,276,293,326,281,7500,Yes,7700,409,0.75,C3
P91,97M1,230,211,232,187,7300,Yes,8800,355,1,C3
HSX,BC32,200,279,276,276,8000,No,8250,295,,C3
C70,GCTM1,242,392,431,375,7500,No,7800,360,,C3
CC6,SS2,201,456,462,375,7000,No,7250,392,,C3
CC7,LL4,267,517,565,479,6400,No,6700,429,,C3
VP1,VV53,230,447,514,427,6300,No,6600,381,,C3
M4G,S58,160,173,173,172,6800,Yes,7500,415,1.7,C3
MGTC,MDA,209,212,212,191,7000,Yes,6700,384,1.35,C3
MGT,MDA,209,217,217,195,7000,Yes,6700,391,,C3
BX5,S6B34,229,304,304,303,7200,Yes,7500,560,1.37,C3
AR8,CPTAV10,250,172,188,180,7800,Yes,8800,416,1.35,C3
LFL,L1R,160,290,337,345,9000,No,9300,401,,C3
LMD,LMV12,232,353,417,393,7300,No,8800,400,,C3
LMH,FSP,250,156,172,169,8000,Yes,8800,401,1.35,C3
AMV,M17,209,133,180,173,8000,Yes,7300,382,1.35,C3
290C,BB53,140,288,301,222,7000,Yes,7300,327,0.75,C3
B8I,38B,210,239,245,238,6500,Yes,6800,331,0.65,C3
Z40,RV30,240,265,266,236,6800,Yes,7700,400,1.03,C3
GLW,15M7,220,356,353,346,6500,Yes,6800,544,1,C3
FGT,EBT,205,260,287,298,7000,Yes,6800,413,0.6,C4
MLN,M4T,170,186,185,180,8500,Yes,8800,442,1.3,C4
LMA,53L,235,427,515,478,8500,No,8800,514,,C4
PGT,M275A,230,184,191,189,9000,Yes,9300,419,1,C4
DX8*,BM13*,120,246,243,223,8300,No,8500,247,,C2
IF6*,RV30*,195,312,311,305,6800,Yes,7100,400,0.5,C3
33R*,BR26*,280,165,263,206,7800,Yes,8000,296,0.6,C2
No Car,R20,190,171,176,160,7200,No,7400,150,,
M34,BS38,150,214,247,333,6900,No,7300,340,,
VPR,VV53,323,446,464,514,6200,No,6500,454,,
HNG,R41Y,220,660,667,658,8000,No,8300,720,,
7RS*,E82A*,190,373,387,348,6700,Yes,7000,468,0.6,C3
BZ4,BS38*,220,304,323,311,8000,No,8300,344,,C3
CVL*,LL6S*,270,530,541,486,6200,No,6500,421,,C3
YRS*,G1E6*,120,142,143,136,7200,Yes,7600,270,1,C3
HRD*,FC3*,195,243,293,287,7200,Yes,7500,418,0.7,C3"""

def calculate_turbo_torque(row):
    """Calculate actual torque for turbocharged engines"""
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
    df['Max Torque'] = df.apply(calculate_turbo_torque, axis=1)
    df['Torque to Weight'] = df['Max Torque'] / df['Engine Weight (KG)']
    df['Power to Weight'] = df['HorsePower'] / df['Engine Weight (KG)']
    df['Is Turbo'] = df['Turbo'].str.lower() == 'yes'
    df['Max Torque'] = df['Max Torque'].round(2)
    df['Torque to Weight'] = df['Torque to Weight'].round(3)
    df['Power to Weight'] = df['Power to Weight'].round(3)
    return df

# Header
st.markdown("<h1 style='text-align:center;color:#f97316;'>🏁 Racing Engine Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#9ca3af;'>Analyzing 105 racing engines with turbo boost calculations</p>", unsafe_allow_html=True)

# Load embedded data
df = pd.read_csv(io.StringIO(CSV_DATA))
df = process_data(df)

# Get data ranges
weight_min, weight_max = float(df['Engine Weight (KG)'].min()), float(df['Engine Weight (KG)'].max())
torque_min, torque_max = float(df['Max Torque'].min()), float(df['Max Torque'].max())
hp_min, hp_max = float(df['HorsePower'].min()), float(df['HorsePower'].max())
tw_min, tw_max = 0.0, float(df['Torque to Weight'].max())

# Sidebar filters
st.sidebar.header("🎛️ Filters")

# Search
search = st.sidebar.text_input("🔍 Search Engine/Car", "")

# Turbo filter
turbo = st.sidebar.radio("Turbo Type", ["All", "Turbo Only", "NA Only"])

# Sort options
sort_by = st.sidebar.selectbox("Sort By", ["Torque to Weight", "Max Torque", "HorsePower", "Power to Weight", "Engine Weight (KG)"])

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Performance Ranges")

# Weight sliders
st.sidebar.markdown("**Weight (kg)**")
weight_max_slider = st.sidebar.slider(
    "Maximum Weight",
    weight_min, weight_max, weight_max,
    key="weight_max",
    help="Set maximum weight - slide left to reduce"
)
weight_min_slider = st.sidebar.slider(
    "Minimum Weight",
    weight_min, weight_max_slider, weight_min,
    key="weight_min",
    help="Set minimum weight (optional)"
)

# Torque sliders
st.sidebar.markdown("**Max Torque (Nm)**")
torque_max_slider = st.sidebar.slider(
    "Maximum Torque",
    torque_min, torque_max, torque_max,
    key="torque_max",
    help="Set maximum torque - slide left to reduce"
)
torque_min_slider = st.sidebar.slider(
    "Minimum Torque",
    torque_min, torque_max_slider, torque_min,
    key="torque_min",
    help="Set minimum torque (optional)"
)

# Horsepower sliders
st.sidebar.markdown("**Horsepower**")
hp_max_slider = st.sidebar.slider(
    "Maximum HP",
    hp_min, hp_max, hp_max,
    key="hp_max",
    help="Set maximum horsepower - slide left to reduce"
)
hp_min_slider = st.sidebar.slider(
    "Minimum HP",
    hp_min, hp_max_slider, hp_min,
    key="hp_min",
    help="Set minimum horsepower (optional)"
)

# Torque to Weight sliders
st.sidebar.markdown("**Torque/Weight Ratio**")
tw_max_slider = st.sidebar.slider(
    "Maximum T/W",
    tw_min, tw_max, tw_max,
    step=0.1,
    key="tw_max",
    help="Set maximum T/W ratio - slide left to reduce"
)
tw_min_slider = st.sidebar.slider(
    "Minimum T/W",
    tw_min, tw_max_slider, tw_min,
    step=0.1,
    key="tw_min",
    help="Set minimum T/W ratio (optional)"
)

# Apply filters
filtered = df.copy()

if search:
    filtered = filtered[
        filtered['Engine'].str.contains(search, case=False, na=False) |
        filtered['Car'].str.contains(search, case=False, na=False)
    ]

if turbo == "Turbo Only":
    filtered = filtered[filtered['Is Turbo']]
elif turbo == "NA Only":
    filtered = filtered[~filtered['Is Turbo']]

# Apply range filters
filtered = filtered[
    (filtered['Engine Weight (KG)'] >= weight_min_slider) &
    (filtered['Engine Weight (KG)'] <= weight_max_slider) &
    (filtered['Max Torque'] >= torque_min_slider) &
    (filtered['Max Torque'] <= torque_max_slider) &
    (filtered['HorsePower'] >= hp_min_slider) &
    (filtered['HorsePower'] <= hp_max_slider) &
    (filtered['Torque to Weight'] >= tw_min_slider) &
    (filtered['Torque to Weight'] <= tw_max_slider)
]

filtered = filtered.sort_values(sort_by, ascending=False).reset_index(drop=True)

# Summary metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Engines", len(filtered))
with col2:
    st.metric("⚡ Turbocharged", int(filtered['Is Turbo'].sum()))
with col3:
    st.metric("Avg T/W Ratio", f"{filtered['Torque to Weight'].mean():.2f}" if len(filtered) > 0 else "N/A")
with col4:
    st.metric("Avg HP", f"{filtered['HorsePower'].mean():.0f}" if len(filtered) > 0 else "N/A")

# Info box about classes
st.info("ℹ️ **Class Information:** Classes (C1-C5) indicate the performance tier of each engine. This is informational only and helps identify which category each engine belongs to.")

st.markdown("---")

# Top 3 Podium
if len(filtered) >= 3:
    st.subheader("🏆 Top 3 Performers")
    top_cols = st.columns(3)
    
    for idx in range(3):
        eng = filtered.iloc[idx]
        with top_cols[idx]:
            emoji = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉"
            turbo_badge = "⚡ TURBO" if eng['Is Turbo'] else "NA"
            
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; 
                        border-left: 4px solid {"#fbbf24" if idx==0 else "#d1d5db" if idx==1 else "#f59e0b"};'>
                <h2 style='margin: 0;'>{emoji} {eng['Engine']}</h2>
                <p style='color: #9ca3af; margin: 5px 0;'>{eng['Car']} • {eng['Class']} • {turbo_badge}</p>
                <h1 style='color: #3b82f6; margin: 10px 0;'>{eng['Torque to Weight']:.2f}</h1>
                <p style='color: #9ca3af; margin: 0;'>Nm/kg</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")

# Display all engines
if len(filtered) > 0:
    st.subheader(f"All Engines (Sorted by {sort_by})")

    for idx, eng in filtered.iterrows():
        rank = idx + 1
        emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
        turbo_icon = " ⚡" if eng['Is Turbo'] else ""
        
        turbo_pressure = eng.get('Turbine Pressure', 0)
        if pd.isna(turbo_pressure):
            turbo_pressure = 0
        boost_info = f" • Boost: {turbo_pressure} bar" if eng['Is Turbo'] and turbo_pressure > 0 else ""
        
        # Color based on rank
        border_color = "#fbbf24" if rank == 1 else "#d1d5db" if rank == 2 else "#f59e0b" if rank == 3 else "#4b5563"
        
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.03); padding: 15px; border-radius: 10px; 
                    border-left: 4px solid {border_color}; margin-bottom: 10px;'>
            <h3 style='margin: 0;'>{emoji} {eng['Engine']}{turbo_icon}</h3>
            <p style='color: #9ca3af; margin: 5px 0;'><strong>{eng['Car']}</strong> • Class: {eng['Class']}{boost_info}</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("T/W Ratio", f"{eng['Torque to Weight']:.2f}")
        c2.metric("Max Torque", f"{eng['Max Torque']:.0f} Nm")
        c3.metric("Weight", f"{eng['Engine Weight (KG)']:.0f} kg")
        c4.metric("Horsepower", f"{eng['HorsePower']:.0f} HP")
        c5.metric("Peak RPM", f"{int(eng['Peak RPM'])}")
        c6.metric("Rev Limiter", f"{int(eng['Rev Limiter'])}")
        
        st.markdown("---")
else:
    st.warning("⚠️ No engines match the current filters. Try adjusting the sliders or filters.")

# Footer
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 20px; margin-top: 40px;'>
    <p>🏁 Racing Engine Performance Dashboard</p>
    <p style='font-size: 12px;'>Turbo boost calculated: Actual Torque = Base Torque + (Base Torque × Turbine Pressure)</p>
</div>
""", unsafe_allow_html=True)
