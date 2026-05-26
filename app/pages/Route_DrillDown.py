import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Route Drill-Down', layout='wide')
st.title('🔎 Route Drill-Down')

if 'filtered_df' not in st.session_state:
    st.warning('Please go to the Home page first.'); st.stop()

filtered = st.session_state['filtered_df']
if len(filtered) == 0:
    st.error('No data under current filters.'); st.stop()

# Selectors
col1, col2 = st.columns(2)
with col1:
    factory_options = ['(All)'] + sorted(filtered['Factory'].dropna().unique().tolist())
    factory = st.selectbox('Factory', factory_options)
with col2:
    state_options = ['(All)'] + sorted(filtered['State/Province'].unique().tolist())
    state = st.selectbox('State', state_options)

drill = filtered.copy()
if factory != '(All)':
    drill = drill[drill['Factory'] == factory]
if state != '(All)':
    drill = drill[drill['State/Province'] == state]

if len(drill) == 0:
    st.warning('No orders match this combination.'); st.stop()

# Headline KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric('Orders', f"{len(drill):,}")
c2.metric('Avg LT', f"{drill['Shipping Lead Time'].mean():.1f} d")
c3.metric('Sales', f"${drill['Sales'].sum():,.0f}")
c4.metric('Profit', f"${drill['Gross Profit'].sum():,.0f}")

st.divider()

# Lead time distribution
fig = px.histogram(drill, x='Shipping Lead Time', nbins=30,
                   title=f'Lead Time Distribution — {factory} → {state}')
st.plotly_chart(fig, use_container_width=True)

# Order timeline
st.subheader('Order Timeline')
timeline = drill.copy().sort_values('Order Date')
fig2 = px.scatter(
    timeline, x='Order Date', y='Shipping Lead Time',
    color='Ship Mode', size='Sales',
    hover_data=['Product Name', 'City'],
    title='Orders Over Time'
)
st.plotly_chart(fig2, use_container_width=True)

# Product breakdown
st.subheader('Product Breakdown')
prod = drill.groupby('Product Name').agg(
    Orders=('Order ID', 'count'),
    Avg_LT=('Shipping Lead Time', 'mean'),
    Total_Sales=('Sales', 'sum')
).round(2).sort_values('Orders', ascending=False)
st.dataframe(prod, use_container_width=True)

# Raw data table
with st.expander('📋 View raw orders'):
    st.dataframe(drill[[
        'Order Date', 'Order ID', 'Factory', 'State/Province',
        'Ship Mode', 'Product Name', 'Shipping Lead Time',
        'Sales', 'Units', 'Gross Profit'
    ]].sort_values('Order Date', ascending=False), use_container_width=True)