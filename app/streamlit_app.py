import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

st.set_page_config(
    page_title='Nassau Candy — Shipping Analytics',
    page_icon='🍬',
    layout='wide',
    initial_sidebar_state='expanded'
)

# ---------- Data loading (cached) ----------
@st.cache_data
def load_data():
    base = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    df = pd.read_csv(os.path.join(base, 'cleaned_data.csv'))
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    route_kpis = pd.read_csv(os.path.join(base, 'route_state_kpis.csv'))
    state_perf = pd.read_csv(os.path.join(base, 'state_performance.csv'))
    return df, route_kpis, state_perf

df, route_kpis, state_perf = load_data()

# ---------- Sidebar Filters ----------
st.sidebar.header('🎯 Filters')

# Date range
min_date, max_date = df['Order Date'].min(), df['Order Date'].max()
date_range = st.sidebar.date_input(
    'Date range',
    value=(min_date.date(), max_date.date()),
    min_value=min_date.date(),
    max_value=max_date.date()
)

# Region
all_regions = sorted(df['Region'].unique())
selected_regions = st.sidebar.multiselect('Region', all_regions, default=all_regions)

# Ship Mode
all_modes = sorted(df['Ship Mode'].unique())
selected_modes = st.sidebar.multiselect('Ship Mode', all_modes, default=all_modes)

# Lead-time threshold for delay
delay_threshold = st.sidebar.slider('Delay threshold (days)', 1, 30, 7)

# Apply filters
def filter_df(df):
    mask = (
        (df['Order Date'] >= pd.Timestamp(date_range[0])) &
        (df['Order Date'] <= pd.Timestamp(date_range[1])) &
        (df['Region'].isin(selected_regions)) &
        (df['Ship Mode'].isin(selected_modes))
    )
    return df[mask]

filtered = filter_df(df)

# ---------- Make filtered data available across pages ----------
st.session_state['filtered_df'] = filtered
st.session_state['delay_threshold'] = delay_threshold
st.session_state['route_kpis'] = route_kpis
st.session_state['state_perf'] = state_perf

# ---------- Home Page ----------
st.title('🍬 Nassau Candy Distributor — Shipping Analytics')
st.markdown('Factory-to-customer shipping route efficiency dashboard')

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric('Total Orders', f"{len(filtered):,}")
with col2:
    st.metric('Avg Lead Time', f"{filtered['Shipping Lead Time'].mean():.1f} days")
with col3:
    delay_rate = (filtered['Shipping Lead Time'] > delay_threshold).mean() * 100
    st.metric('Delay Rate', f"{delay_rate:.1f}%")
with col4:
    st.metric('Total Sales', f"${filtered['Sales'].sum():,.0f}")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.metric('Total Units Shipped', f"{filtered['Units'].sum():,}")
with col2:
    st.metric('Total Gross Profit', f"${filtered['Gross Profit'].sum():,.0f}")

st.divider()
st.markdown("""
### 📍 Navigation
Use the left sidebar to navigate between pages:
- **Route Overview** — Top/bottom routes, leaderboards
- **Geographic Map** — US heatmap and route network
- **Ship Mode Comparison** — Performance across shipping classes
- **Route Drill-Down** — Detailed state-level analysis
""")

# Recent orders
st.subheader('📋 Recent Orders (Filtered)')
st.dataframe(
    filtered.sort_values('Order Date', ascending=False).head(20)[
        ['Order Date', 'Order ID', 'Region', 'State/Province', 'Ship Mode',
         'Factory', 'Product Name', 'Shipping Lead Time', 'Sales']
    ],
    use_container_width=True
)