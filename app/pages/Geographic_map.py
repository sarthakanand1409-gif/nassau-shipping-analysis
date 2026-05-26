import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from visualization import plot_us_choropleth, plot_route_network_map, plot_volume_vs_leadtime

st.set_page_config(page_title='Geographic Map', layout='wide')
st.title('🗺️ Geographic Shipping Analysis')

if 'filtered_df' not in st.session_state:
    st.warning('Please go to the Home page first to set filters.')
    st.stop()

filtered = st.session_state['filtered_df']
state_perf = st.session_state['state_perf']

if len(filtered) == 0:
    st.error('No data matches the current filters.'); st.stop()

# Recompute state-level performance from filtered data
sp = filtered.groupby('State/Province').agg(
    Avg_Lead_Time=('Shipping Lead Time', 'mean'),
    Volume=('Order ID', 'count'),
    Total_Sales=('Sales', 'sum'),
    Avg_Profit_Margin=('Profit Margin %', 'mean')
).reset_index().round(2)

# Reuse same threshold logic
ltt = sp['Avg_Lead_Time'].quantile(0.75)
vt = sp['Volume'].quantile(0.75)
sp['Is_Bottleneck'] = (sp['Avg_Lead_Time'] >= ltt) & (sp['Volume'] >= vt)
sp['Performance_Category'] = sp.apply(
    lambda r: 'Critical Bottleneck' if r['Is_Bottleneck']
    else 'Slow Route' if r['Avg_Lead_Time'] >= ltt
    else 'High-Volume Healthy' if r['Volume'] >= vt
    else 'Standard', axis=1
)

# Metric selector
metric = st.selectbox('Choropleth metric', ['Avg_Lead_Time', 'Volume', 'Total_Sales'])
st.plotly_chart(plot_us_choropleth(sp, metric=metric), use_container_width=True)

st.divider()
st.subheader('Volume vs. Lead Time by State')
st.plotly_chart(plot_volume_vs_leadtime(sp), use_container_width=True)

st.divider()
st.subheader('Top Routes (Network View)')
top_n = st.slider('Routes to display', 5, 50, 20)
st.plotly_chart(plot_route_network_map(filtered, top_n=top_n), use_container_width=True)

st.divider()
st.subheader('🚨 Critical Bottlenecks')
bottlenecks = sp[sp['Performance_Category']  =='Critical Bottleneck'].sort_values('Volume', ascending=False)
if len(bottlenecks) == 0:
    st.success('No critical bottlenecks under current filters.')
else:
    st.dataframe(bottlenecks, use_container_width=True, hide_index=True)