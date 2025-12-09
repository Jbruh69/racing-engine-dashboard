import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import io

# Page setup
st.set_page_config(page_title="🏁 Racing Engine Dashboard", page_icon="🏁", layout="wide")

# ============== EMBEDDED DATA ==============

ENGINE_DATA = """Car,Engine,Engine Weight (KG),Low Torque(Nm),Medium Torque(Nm),High Torque(Nm),Rev Limiter,Turbo,Peak RPM,HorsePower,Turbine Pressure,Class
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

CHASSIS_DATA = """Car,Weight,Front Aero,Rear Aero,Class,Max Wheel Size,Drivetrain,Weight Dist Front/Rear
HC6,1077,32,38,C1,,FF,60/40
NX5,1082,32,38,C1,,FR,52/48
DTS,1180,32,37,C1,,FR,56/44
NX5C,1084,32,38,C1,,FR,51/49
PF7,1480,35,41,C1,,FR,53/47
ECL,1295,31,36,C1,,FF,59/41
E86,955,35,41,C1,,FR,55/45
2MR,1187,33,39,C1,,MR,44/56
B19,1170,28,33,C1,,FR,52/48
FLD,901,35,41,C1,,FR,52/48
E36,1260,35,41,C1,,FR,51/49
20R,946,35,41,C1,,FR,50/50
30Z,1336,38,45,C1,,FR,51/49
S18,1012,35,41,C1,,FR,57/43
V7G,1235,33,39,C1,,FF,62/38
G86,1120,35,41,C1,,FR,55/45
MCS,1020,32,38,C1,,FF,62/38
SFR,1380,40,47,C1,325/R20,FAWD,55/45
30ZC,1336,38,45,C1,,FR,51/49
FX7,1127,34,40,C2,,FR,50/50
Z31,1252,32,38,C2,,FR,53/47
M46,1421,35,41,C2,,FR,50/50
CHR,1464,33,39,C2,,FR,55/45
32R,1185,35,41,C2,,FAWD,58/42
R86,1309,36,42,C2,,FR,53/47
FST,1393,33,39,C2,,FF,61/39
CRN,1465,31,36,C2,,FR,56/44
M30,1029,34,40,C2,,FR,52/48
WRS,1495,35,41,C2,,FAWD,57/43
S14,1100,32,37,C2,,FR,56/44
HC9,886,34,40,C2,,FF,65/35
HCR,1349,35,41,C2,,FF,61/39
TTR,1450,34,40,C2,,FAWD,59/41
S13,990,36,42,C2,,FR,50/50
S15,1140,33,39,C2,,FR,52/48
S80,1360,35,41,C2,,FR,54/46
P64,1330,32,38,C2,,RR,38/62
DC2,1766,35,41,C2,,FR,54/46
HI5,1000,32,38,C2,,FF,61/39
Z35,1340,36,42,C2,,FR,53/47
Z37,1384,35,41,C2,,FR,53/47
TM2,1280,32,38,C2,,FR,52/48
CRT,1270,32,38,C2,,FR,52/48
HS2,1123,31,36,C2,,FR,50/50
F69,1364,33,39,C2,,FR,58/42
34R,1380,35,41,C2,,FR,58/42
EV9,1245,36,42,C2,,FAWD,59/41
EVX,1416,35,43,C2,,FAWD,57/43
WST,1236,36,42,C2,,FAWD,58/42
M92,1595,36,42,C2,,FR,52/48
CMR,1568,39,46,C2,,FR,55/45
M39,1562,29,34,C2,,FR,55/45
M92C,1615,36,42,C2,,FR,52/48
63C,1710,37,43,C3,,FR,53/47
EV6,1190,32,37,C3,,FAWD,60/40
B31,1700,33,39,C3,,FR,52/48
S90,1401,37,43,C3,,FR,50/50
F35,1510,38,45,C3,,FR,50/50
S65,1609,40,47,C3,,FR,53/47
DX7,1144,34,40,C3,,FR,50/50
6RS,1825,36,42,C3,,FAWD,54/46
STR,1725,35,41,C3,,FR,56/44
M4R,1477,35,41,C3,,FR,50/50
B60,1580,40,43,C3,,FR,52/48
HSS,1643,35,41,C3,,FR,52/48
BM2,1376,40,47,C3,,FR,50/50
M90,1701,31,36,C3,,FAWD,54/46
35R,1588,40,47,C3,,FAWD,53/47
P91,1345,33,39,C3,,RR,40/60
HSX,1110,37,43,C3,,MR,42/58
C70,1288,32,37,C3,,FR,57/43
CC6,1399,39,46,C3,,FR,54/46
CC7,1467,46,54,C3,,FR,50/50
VP1,1335,38,45,C3,,FR,50/50
M4G,1655,37,44,C3,,FR,50/50
MGTC,1491,42,50,C3,,FR,50/50
MGT,1436,42,50,C3,,FR,49/51
BX5,2246,32,37,C3,,FAWD,50/50
AR8,1420,42,49,C3,,MAWD,43/57
LFL,1456,42,49,C3,,FMR,50/50
LMD,1393,32,38,C3,,MR,43/57
LMH,1340,44,52,C3,,MR,40/60
AMV,1321,43,51,C3,,MR,49/51
S90C,1451,37,43,C3,,FR,50/50
B8I,1275,38,43,C3,,FR,50/50
Z40,1394,34,40,C3,,FR,56/44
GLW,2330,29,35,C3,,FAWD,58/42
FGT,1195,48,52,C4,,RMR,43/57
MLN,1315,47,51,C4,,MR,42/58
LMA,1505,44,51,C4,,MR,43/57
PGT,1205,46,50,C4,,RR,40/60
DX8*,1190,36,42,C2,,FR,50/50
IF6*,1719,35,39,C3,,FAWD,58/42
33R*,1250,38,44,C2,,FR,51/49
HNG*,,37,39,C6,,,
M34*,,37,42,C3,,,
VPR*,,41,47,,,,
7RS*,1960,36,41,C3,,FAWD,54/46
BZ4*,1275,38,43,C3,,FR,49/51
CVL*,1480,36,38,C3,,FR,55/45
YRS*,1160,35,41,C3,,FAWD,54/46"""

# ============== DATA PROCESSING ==============

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

def get_torque_curve_data(row):
    """Generate torque curve points for a vehicle"""
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
    
    rev_limit = row.get('Rev Limiter', 7000)
    peak_rpm = row.get('Peak RPM', 7500)
    
    rpm_points = [1000, 2000, 3000, int(rev_limit * 0.5), int(rev_limit * 0.7), int(rev_limit * 0.85), int(peak_rpm), int(rev_limit)]
    torque_points = [
        low * 0.6,
        low * 0.85,
        low,
        med * 0.95,
        med,
        high * 0.98,
        high,
        high * 0.85
    ]
    
    return rpm_points, torque_points

def process_engine_data(df):
    df['Max Torque'] = df.apply(calculate_turbo_torque, axis=1)
    df['Torque to Weight'] = df['Max Torque'] / df['Engine Weight (KG)']
    df['Power to Weight'] = df['HorsePower'] / df['Engine Weight (KG)']
    df['Is Turbo'] = df['Turbo'].str.lower() == 'yes'
    df['Max Torque'] = df['Max Torque'].round(2)
    df['Torque to Weight'] = df['Torque to Weight'].round(3)
    df['Power to Weight'] = df['Power to Weight'].round(3)
    return df

def process_chassis_data(df):
    df['Total Aero'] = df['Front Aero'] + df['Rear Aero']
    df['Aero Balance'] = (df['Front Aero'] / df['Total Aero'] * 100).round(1)
    return df

# Load data
engine_df = pd.read_csv(io.StringIO(ENGINE_DATA))
engine_df = process_engine_data(engine_df)

chassis_df = pd.read_csv(io.StringIO(CHASSIS_DATA))
chassis_df = process_chassis_data(chassis_df)

# ============== HEADER ==============

st.markdown("<h1 style='text-align:center;color:#f97316;'>🏁 Racing Engine Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#9ca3af;'>Analyzing 105 racing engines with turbo boost calculations</p>", unsafe_allow_html=True)

# ============== TABS ==============

tab1, tab2, tab3, tab4 = st.tabs(["🔧 Engines", "📊 Compare", "⚖️ Weight", "💨 Aero"])

# ============== TAB 1: ENGINES ==============

with tab1:
    # Get data ranges
    weight_min, weight_max = float(engine_df['Engine Weight (KG)'].min()), float(engine_df['Engine Weight (KG)'].max())
    torque_min, torque_max = float(engine_df['Max Torque'].min()), float(engine_df['Max Torque'].max())
    hp_min, hp_max = float(engine_df['HorsePower'].min()), float(engine_df['HorsePower'].max())
    tw_min, tw_max = 0.0, float(engine_df['Torque to Weight'].max())

    # Sidebar filters
    st.sidebar.header("🎛️ Filters")

    # Search
    search = st.sidebar.text_input("🔍 Search Engine/Car", "")

    # Turbo filter
    turbo = st.sidebar.radio("Turbo Type", ["All", "Turbo Only", "NA Only"])

    # Sort options
    sort_by = st.sidebar.selectbox("Sort By", ["Torque to Weight", "Max Torque", "HorsePower", "Power to Weight", "Engine Weight (KG)"])
    sort_order = st.sidebar.radio("Order", ["Descending", "Ascending"], key="eng_order")

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

    # Max Torque sliders
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
    filtered = engine_df.copy()

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

    filtered = filtered.sort_values(sort_by, ascending=(sort_order == "Ascending")).reset_index(drop=True)

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
        st.subheader(f"🏆 Top 3 by {sort_by} ({sort_order})")
        top_cols = st.columns(3)
        
        for idx in range(3):
            eng = filtered.iloc[idx]
            with top_cols[idx]:
                emoji = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉"
                turbo_badge = "⚡ TURBO" if eng['Is Turbo'] else "NA"
                class_val = eng['Class'] if pd.notna(eng['Class']) else "N/A"
                
                # Display the value being sorted by
                if sort_by == "Torque to Weight":
                    display_val = f"{eng['Torque to Weight']:.2f}"
                    display_unit = "Nm/kg"
                elif sort_by == "Max Torque":
                    display_val = f"{eng['Max Torque']:.0f}"
                    display_unit = "Nm"
                elif sort_by == "HorsePower":
                    display_val = f"{eng['HorsePower']:.0f}"
                    display_unit = "HP"
                elif sort_by == "Power to Weight":
                    display_val = f"{eng['Power to Weight']:.2f}"
                    display_unit = "HP/kg"
                else:  # Engine Weight
                    display_val = f"{eng['Engine Weight (KG)']:.0f}"
                    display_unit = "kg"
                
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; 
                            border-left: 4px solid {"#fbbf24" if idx==0 else "#d1d5db" if idx==1 else "#f59e0b"};'>
                    <h2 style='margin: 0;'>{emoji} {eng['Engine']}</h2>
                    <p style='color: #9ca3af; margin: 5px 0;'>{eng['Car']} • {class_val} • {turbo_badge}</p>
                    <h1 style='color: #3b82f6; margin: 10px 0;'>{display_val}</h1>
                    <p style='color: #9ca3af; margin: 0;'>{display_unit}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")

    # Display all engines
    if len(filtered) > 0:
        st.subheader(f"All Engines (Sorted by {sort_by} - {sort_order})")

        for idx, eng in filtered.iterrows():
            rank = filtered.index.get_loc(idx) + 1
            
            # Show podium medals for top 3
            emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
            border_color = "#fbbf24" if rank == 1 else "#d1d5db" if rank == 2 else "#f59e0b" if rank == 3 else "#4b5563"
            turbo_icon = " ⚡" if eng['Is Turbo'] else ""
            
            turbo_pressure = eng.get('Turbine Pressure', 0)
            if pd.isna(turbo_pressure):
                turbo_pressure = 0
            boost_info = f" • Boost: {turbo_pressure} bar" if eng['Is Turbo'] and turbo_pressure > 0 else ""
            
            class_val = eng['Class'] if pd.notna(eng['Class']) else "N/A"
            
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.03); padding: 15px; border-radius: 10px; 
                        border-left: 4px solid {border_color}; margin-bottom: 10px;'>
                <h3 style='margin: 0;'>{emoji} {eng['Engine']}{turbo_icon}</h3>
                <p style='color: #9ca3af; margin: 5px 0;'><strong>{eng['Car']}</strong> • Class: {class_val}{boost_info}</p>
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

# ============== TAB 2: COMPARE ==============

with tab2:
    st.subheader("📊 Vehicle Torque Curve Comparison")
    st.markdown("Select vehicles to compare their hypothetical torque curves")
    
    # Create combined Car + Engine labels for selection
    engine_df['Selection Label'] = engine_df['Car'] + " (" + engine_df['Engine'] + ")"
    available_options = engine_df['Selection Label'].unique().tolist()
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        selected_options = st.multiselect(
            "Select by Car or Engine Name (max 6)",
            available_options,
            default=available_options[:3] if len(available_options) >= 3 else available_options,
            max_selections=6,
            key="compare_cars"
        )
    with col_sel2:
        chart_height = st.slider("Chart Height", 400, 800, 500, key="chart_height")
    
    # Convert selected options back to car names
    selected_cars = [opt.split(" (")[0] for opt in selected_options]
    
    if selected_cars:
        # Create torque curve chart
        fig = go.Figure()
        
        colors = ['#3b82f6', '#ef4444', '#22c55e', '#f59e0b', '#8b5cf6', '#ec4899']
        
        for i, car in enumerate(selected_cars):
            car_data = engine_df[engine_df['Car'] == car].iloc[0]
            rpm_points, torque_points = get_torque_curve_data(car_data)
            
            turbo_label = " ⚡" if car_data['Is Turbo'] else ""
            
            fig.add_trace(go.Scatter(
                x=rpm_points,
                y=torque_points,
                mode='lines+markers',
                name=f"{car} ({car_data['Engine']}){turbo_label}",
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=8),
                hovertemplate=f"<b>{car}</b><br>RPM: %{{x}}<br>Torque: %{{y:.0f}} Nm<extra></extra>"
            ))
        
        fig.update_layout(
            title=dict(text="Torque Curves Comparison", font=dict(size=20)),
            xaxis_title="RPM",
            yaxis_title="Torque (Nm)",
            height=chart_height,
            template="plotly_dark",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Side by side stats in card format
        st.markdown("### 📈 Quick Stats")
        stat_cols = st.columns(len(selected_cars))
        
        for i, car in enumerate(selected_cars):
            car_data = engine_df[engine_df['Car'] == car].iloc[0]
            with stat_cols[i]:
                turbo_icon = "⚡" if car_data['Is Turbo'] else "🔧"
                class_val = car_data['Class'] if pd.notna(car_data['Class']) else "N/A"
                
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; 
                            border-left: 4px solid {colors[i % len(colors)]}; margin-bottom: 10px;'>
                    <h3 style='margin: 0;'>{turbo_icon} {car}</h3>
                    <p style='color: #9ca3af; margin: 5px 0;'>{car_data['Engine']} • {class_val}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.metric("Max Torque", f"{car_data['Max Torque']:.0f} Nm")
                st.metric("Horsepower", f"{car_data['HorsePower']:.0f} HP")
                st.metric("T/W Ratio", f"{car_data['Torque to Weight']:.2f}")
                st.metric("Peak RPM", f"{int(car_data['Peak RPM'])}")
    else:
        st.info("👆 Select at least one vehicle to see the torque curve comparison")

# ============== TAB 3: WEIGHT ==============

with tab3:
    st.subheader("⚖️ Chassis Weight Database")
    
    # Filters in sidebar style
    st.sidebar.markdown("---")
    st.sidebar.header("⚖️ Weight Filters")
    
    wt_search = st.sidebar.text_input("🔍 Search Car", "", key="wt_search")
    wt_sort = st.sidebar.selectbox("Sort By", ["Weight", "Car"], key="wt_sort")
    wt_order = st.sidebar.radio("Order", ["Ascending", "Descending"], key="wt_order")
    
    # Weight range filter
    valid_weights = chassis_df[chassis_df['Weight'].notna()]['Weight']
    if len(valid_weights) > 0:
        wt_min, wt_max = float(valid_weights.min()), float(valid_weights.max())
        
        st.sidebar.markdown("**Chassis Weight (kg)**")
        wt_max_slider = st.sidebar.slider(
            "Maximum Chassis Weight",
            wt_min, wt_max, wt_max,
            key="wt_max_slider",
            help="Set maximum chassis weight"
        )
        wt_min_slider = st.sidebar.slider(
            "Minimum Chassis Weight",
            wt_min, wt_max_slider, wt_min,
            key="wt_min_slider",
            help="Set minimum chassis weight"
        )
    else:
        wt_min_slider, wt_max_slider = 0, 9999
    
    # Apply filters
    wt_filtered = chassis_df.copy()
    wt_filtered = wt_filtered[wt_filtered['Weight'].notna()]
    
    if wt_search:
        wt_filtered = wt_filtered[wt_filtered['Car'].str.contains(wt_search, case=False, na=False)]
    
    wt_filtered = wt_filtered[
        (wt_filtered['Weight'] >= wt_min_slider) &
        (wt_filtered['Weight'] <= wt_max_slider)
    ]
    
    ascending = wt_order == "Ascending"
    wt_filtered = wt_filtered.sort_values(wt_sort, ascending=ascending).reset_index(drop=True)
    
    # Summary
    wm1, wm2, wm3, wm4 = st.columns(4)
    with wm1:
        st.metric("Total Vehicles", len(wt_filtered))
    with wm2:
        st.metric("Lightest", f"{wt_filtered['Weight'].min():.0f} kg" if len(wt_filtered) > 0 else "N/A")
    with wm3:
        st.metric("Heaviest", f"{wt_filtered['Weight'].max():.0f} kg" if len(wt_filtered) > 0 else "N/A")
    with wm4:
        st.metric("Average", f"{wt_filtered['Weight'].mean():.0f} kg" if len(wt_filtered) > 0 else "N/A")
    
    st.markdown("---")
    
    # Display each vehicle in card style
    if len(wt_filtered) > 0:
        st.subheader(f"All Vehicles (Sorted by {wt_sort} - {wt_order})")
        
        for idx, row in wt_filtered.iterrows():
            rank = wt_filtered.index.get_loc(idx) + 1
            
            if wt_order == "Ascending":
                emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
                border_color = "#fbbf24" if rank == 1 else "#d1d5db" if rank == 2 else "#f59e0b" if rank == 3 else "#4b5563"
            else:
                emoji = f"#{rank}"
                border_color = "#4b5563"
            
            class_val = row['Class'] if pd.notna(row['Class']) else "N/A"
            drivetrain = row['Drivetrain'] if pd.notna(row['Drivetrain']) else "N/A"
            weight_dist = row['Weight Dist Front/Rear'] if pd.notna(row['Weight Dist Front/Rear']) else "N/A"
            
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.03); padding: 15px; border-radius: 10px; 
                        border-left: 4px solid {border_color}; margin-bottom: 10px;'>
                <h3 style='margin: 0;'>{emoji} {row['Car']}</h3>
                <p style='color: #9ca3af; margin: 5px 0;'>Class: {class_val} • {drivetrain}</p>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Weight", f"{row['Weight']:.0f} kg")
            c2.metric("Drivetrain", drivetrain)
            c3.metric("Weight Dist", weight_dist)
            
            st.markdown("---")
    else:
        st.warning("⚠️ No vehicles match the current filters.")

# ============== TAB 4: AERO ==============

with tab4:
    st.subheader("💨 Aerodynamics Database")
    
    # Filters in sidebar style
    st.sidebar.markdown("---")
    st.sidebar.header("💨 Aero Filters")
    
    ar_search = st.sidebar.text_input("🔍 Search Car", "", key="ar_search")
    ar_sort = st.sidebar.selectbox("Sort By", ["Total Aero", "Front Aero", "Rear Aero", "Car"], key="ar_sort")
    ar_order = st.sidebar.radio("Order", ["Ascending", "Descending"], key="ar_order")
    
    # Aero range sliders
    st.sidebar.markdown("**Front Aero**")
    front_max = st.sidebar.slider(
        "Maximum Front Aero",
        float(chassis_df['Front Aero'].min()),
        float(chassis_df['Front Aero'].max()),
        float(chassis_df['Front Aero'].max()),
        key="front_max"
    )
    front_min = st.sidebar.slider(
        "Minimum Front Aero",
        float(chassis_df['Front Aero'].min()),
        front_max,
        float(chassis_df['Front Aero'].min()),
        key="front_min"
    )
    
    st.sidebar.markdown("**Rear Aero**")
    rear_max = st.sidebar.slider(
        "Maximum Rear Aero",
        float(chassis_df['Rear Aero'].min()),
        float(chassis_df['Rear Aero'].max()),
        float(chassis_df['Rear Aero'].max()),
        key="rear_max"
    )
    rear_min = st.sidebar.slider(
        "Minimum Rear Aero",
        float(chassis_df['Rear Aero'].min()),
        rear_max,
        float(chassis_df['Rear Aero'].min()),
        key="rear_min"
    )
    
    # Apply filters
    ar_filtered = chassis_df.copy()
    
    if ar_search:
        ar_filtered = ar_filtered[ar_filtered['Car'].str.contains(ar_search, case=False, na=False)]
    
    ar_filtered = ar_filtered[
        (ar_filtered['Front Aero'] >= front_min) &
        (ar_filtered['Front Aero'] <= front_max) &
        (ar_filtered['Rear Aero'] >= rear_min) &
        (ar_filtered['Rear Aero'] <= rear_max)
    ]
    
    ascending = ar_order == "Ascending"
    ar_filtered = ar_filtered.sort_values(ar_sort, ascending=ascending).reset_index(drop=True)
    
    # Summary
    am1, am2, am3, am4 = st.columns(4)
    with am1:
        st.metric("Total Vehicles", len(ar_filtered))
    with am2:
        st.metric("Avg Front Aero", f"{ar_filtered['Front Aero'].mean():.1f}" if len(ar_filtered) > 0 else "N/A")
    with am3:
        st.metric("Avg Rear Aero", f"{ar_filtered['Rear Aero'].mean():.1f}" if len(ar_filtered) > 0 else "N/A")
    with am4:
        st.metric("Avg Total Aero", f"{ar_filtered['Total Aero'].mean():.1f}" if len(ar_filtered) > 0 else "N/A")
    
    st.markdown("---")
    
    # Display each vehicle in card style
    if len(ar_filtered) > 0:
        st.subheader(f"All Vehicles (Sorted by {ar_sort} - {ar_order})")
        
        for idx, row in ar_filtered.iterrows():
            rank = ar_filtered.index.get_loc(idx) + 1
            
            if ar_order == "Descending":
                emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
                border_color = "#fbbf24" if rank == 1 else "#d1d5db" if rank == 2 else "#f59e0b" if rank == 3 else "#4b5563"
            else:
                emoji = f"#{rank}"
                border_color = "#4b5563"
            
            class_val = row['Class'] if pd.notna(row['Class']) else "N/A"
            drivetrain = row['Drivetrain'] if pd.notna(row['Drivetrain']) else "N/A"
            
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.03); padding: 15px; border-radius: 10px; 
                        border-left: 4px solid {border_color}; margin-bottom: 10px;'>
                <h3 style='margin: 0;'>{emoji} {row['Car']}</h3>
                <p style='color: #9ca3af; margin: 5px 0;'>Class: {class_val} • {drivetrain}</p>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Front Aero", f"{row['Front Aero']:.0f}")
            c2.metric("Rear Aero", f"{row['Rear Aero']:.0f}")
            c3.metric("Total Aero", f"{row['Total Aero']:.0f}")
            c4.metric("Aero Balance", f"{row['Aero Balance']:.1f}% F")
            
            st.markdown("---")
    else:
        st.warning("⚠️ No vehicles match the current filters.")

# ============== FOOTER ==============

st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 20px; margin-top: 40px;'>
    <p>🏁 Racing Engine Performance Dashboard</p>
    <p style='font-size: 12px;'>Turbo boost calculated: Actual Torque = Base Torque + (Base Torque × Turbine Pressure)</p>
</div>
""", unsafe_allow_html=True)
