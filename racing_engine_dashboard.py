import streamlit as st
import pandas as pd
import io

# Page setup
st.set_page_config(page_title="🏁 Racing Engine Dashboard", page_icon="🏁", layout="wide")

# Custom CSS for slider styling
st.markdown("""
    <style>
    .stSlider > div > div > div > div {
        background: linear-gradient(to right, #3b82f6 0%, #3b82f6 100%);
    }
    </style>
""", unsafe_allow_html=True)

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
M3G,VAN,199,253,299,251,5600,Yes,5900,201,0.92,C1
TVL,TVL,235,194,177,177,7000,Yes,7300,225,0.7,C1
M3G6,VAN,199,220,250,220,5600,Yes,5900,220,1.2,C1
E60,G06,175,186,223,199,6500,Yes,6800,220,0.7,C1
E60T,C25,205,209,222,213,6500,Yes,6800,249,0.75,C1
HCR,KA20,145,185,203,188,7200,Yes,7500,212,0.8,C1
B30,M93,135,191,191,149,6500,Yes,6900,167,0.65,C2
B30,M92C,135,191,191,149,6500,Yes,6900,167,0.65,C2
FST,RDA,109,120,149,123,7700,Yes,8000,138,0.73,C2
LL1,CMR,193,220,240,223,6500,Yes,6900,232,1.1,C2
F31,S14,167,195,200,181,7300,Yes,7600,195,0.7,C2
E36,S50,165,198,234,220,7200,Yes,7500,240,0.8,C2
FTO,4G63,240,268,286,268,6800,Yes,7200,280,0.68,C2
FCX,F20C,140,161,182,159,8200,Yes,8600,181,0.75,C2
E46,S54,175,269,284,245,8000,Yes,8300,252,0.65,C2
E92,S65,202,295,310,280,8500,Yes,8900,309,0.6,C2
SB70,B31,155,195,218,192,7000,Yes,7300,205,1.45,C3
CC6,SS2,201,214,230,217,6500,Yes,6900,238,1.13,C3
VP1,VV53,230,230,255,230,6100,Yes,6500,260,1.24,C3
LMA,53L,235,220,235,220,6500,Yes,6900,250,1.34,C4
V8S,V10C,310,420,450,410,7000,Yes,7400,480,0.85,C4
G82,S58,245,380,420,390,7200,Yes,7600,503,1,C4
RS6,V8T,280,420,460,430,6800,Yes,7200,560,0.92,C4
M5C,S63,265,420,480,450,7000,Yes,7400,600,1.05,C4
991,MA1,285,420,460,440,8400,Yes,8800,520,0.78,C4
GT3,MA2,198,339,357,339,9000,No,9300,375,,C4
GT4,MA2,198,339,357,339,9000,No,9300,385,,C4
458,F136,202,398,398,343,9000,No,9250,419,,C4
488,F154,195,560,560,505,8000,Yes,8500,670,0.92,C5
STO,LF3,230,565,580,565,8500,Yes,8900,640,0.88,C5
SF90,F163,270,590,620,590,8000,Yes,8500,780,1.15,C5
720S,M840T,198,568,590,568,8500,Yes,8900,710,1.2,C5
765LT,M840T,198,612,640,612,8500,Yes,8900,765,1.35,C5
AMG,M177,230,630,670,630,7200,Yes,7600,730,1.28,C5
P1,M838T,198,664,720,664,8500,Yes,8900,903,1.45,C5
ENZO,F140,225,485,485,418,8200,No,8500,651,,C5
ZONDA,M120,266,553,553,478,7500,No,7900,602,,C5
CGT,M80,252,528,528,456,8400,No,8700,605,,C5
LFA,1LR,285,354,354,306,9000,No,9300,412,,C5"""

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
st.markdown("<p style='text-align:center;color:#9ca3af;'>Analyzing 54 racing engines with turbo boost calculations</p>", unsafe_allow_html=True)

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

# Classes
all_classes = sorted([str(c) for c in df['Class'].unique() if pd.notna(c)])
selected_classes = st.sidebar.multiselect("Classes", all_classes, default=all_classes)

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

if selected_classes:
    filtered = filtered[filtered['Class'].isin(selected_classes)]

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
    st.warning("No engines match the current filters. Try adjusting the sliders or filters.")

# Footer
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 20px; margin-top: 40px;'>
    <p>🏁 Racing Engine Performance Dashboard</p>
    <p style='font-size: 12px;'>Turbo boost calculated: Actual Torque = Base Torque + (Base Torque × Turbine Pressure)</p>
</div>
""", unsafe_allow_html=True)
