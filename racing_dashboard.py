import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="🏁 Racing Engine Dashboard", page_icon="🏁", layout="wide")

def calculate_turbo_torque(row):
    """Calculate actual torque for turbocharged engines
    Formula: Actual torque = base torque + (base torque × turbine pressure)"""
    low = row.get('Low Torque(Nm)', 0)
    med = row.get('Medium Torque(Nm)', 0)
    high = row.get('High Torque(Nm)', 0)
    
    is_turbo = str(row.get('Turbo', '')).lower() == 'yes'
    pressure = row.get('Turbine Pressure', 0) or 0
    
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

# File uploader
uploaded_file = st.file_uploader("Upload your engine CSV file", type=['csv'])

if uploaded_file:
    # Load and process data
    df = pd.read_csv(uploaded_file)
    df = process_data(df)
    
    # Sidebar filters
    st.sidebar.header("🎛️ Filters")
    search = st.sidebar.text_input("🔍 Search", "")
    classes = st.sidebar.multiselect("Classes", sorted(df['Class'].unique()), default=list(df['Class'].unique()))
    turbo = st.sidebar.radio("Turbo Type", ["All", "Turbo Only", "NA Only"])
    sort_by = st.sidebar.selectbox("Sort By", ["Torque to Weight", "Max Torque", "HorsePower", "Power to Weight"])
    
    # Apply filters
    filtered = df.copy()
    
    if search:
        filtered = filtered[
            filtered['Engine'].str.contains(search, case=False, na=False) |
            filtered['Car'].str.contains(search, case=False, na=False)
        ]
    
    filtered = filtered[filtered['Class'].isin(classes)]
    
    if turbo == "Turbo Only":
        filtered = filtered[filtered['Is Turbo']]
    elif turbo == "NA Only":
        filtered = filtered[~filtered['Is Turbo']]
    
    filtered = filtered.sort_values(sort_by, ascending=False).reset_index(drop=True)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Engines", len(filtered))
    with col2:
        st.metric("⚡ Turbocharged", filtered['Is Turbo'].sum())
    with col3:
        st.metric("Avg T/W Ratio", f"{filtered['Torque to Weight'].mean():.2f}")
    with col4:
        st.metric("Avg HP", f"{filtered['HorsePower'].mean():.0f}")
    
    st.markdown("---")
    
    # Display engines
    for idx, eng in filtered.iterrows():
        rank = idx + 1
        emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
        turbo_icon = " ⚡" if eng['Is Turbo'] else ""
        boost_info = f" • Boost: {eng['Turbine Pressure']} bar" if eng['Is Turbo'] and eng['Turbine Pressure'] > 0 else ""
        
        st.markdown(f"### {emoji} {eng['Engine']}{turbo_icon}")
        st.write(f"**{eng['Car']}** • Class: {eng['Class']}{boost_info}")
        
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("T/W Ratio", f"{eng['Torque to Weight']:.2f}")
        c2.metric("Max Torque", f"{eng['Max Torque']} Nm")
        c3.metric("Weight", f"{eng['Engine Weight (KG)']} kg")
        c4.metric("Horsepower", f"{eng['HorsePower']} HP")
        c5.metric("Peak RPM", f"{eng['Peak RPM']}")
        c6.metric("Rev Limiter", f"{eng['Rev Limiter']}")
        st.markdown("---")
else:
    st.info("👆 Upload your CSV file to get started!")
    st.markdown("""
    **Expected CSV columns:**
```
    Car, Engine, Engine Weight (KG), Low Torque(Nm), Medium Torque(Nm), 
    High Torque(Nm), Rev Limiter, Turbo, Peak RPM, HorsePower, 
    Turbine Pressure, Class
```
    
    **⚡ Turbo Calculation:**  
    For turbocharged engines: `Actual Torque = Base Torque + (Base Torque × Turbine Pressure)`
    """)