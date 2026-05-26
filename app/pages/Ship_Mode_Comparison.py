import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from visualization import plot_lead_time_by_ship_mode, plot_ship_mode_region_heatmap

st.set_page_config(page_title='Ship Mode Comparison', layout='wide')
st.title('🚚 Ship Mode Performance')

if 'filtered_df' not in st.session_state:
    st.warning('Please go to the Home page first.'); st.stop()

filtered = st.session_state['filtered_df']
if len(filtered) == 0:
    st.error('No data under current filters.'); st.stop()

# Summary table
mode_summary = filtered.groupby('Ship Mode').agg(
    Volume=('Order ID', 'count'),
    Avg_Lead_Time=('Shipping Lead Time', 'mean'),
    Median_Lead_Time=('Shipping Lead Time', 'median'),
    Lead_Time_Std=('Shipping Lead Time', 'std'),
    Total_Sales=('Sales', 'sum'),
    Avg_Sales_Per_Order=('Sales', 'mean'),
    Avg_Profit_Margin=('Profit Margin %', 'mean')
).round(2).reset_index()
mode_summary['Volume_%'] = (mode_summary['Volume'] / mode_summary['Volume'].sum() * 100).round(2)
mode_summary = mode_summary.sort_values('Avg_Lead_Time')

st.subheader('Ship Mode KPI Summary')
st.dataframe(mode_summary, use_container_width=True, hide_index=True)

st.divider()
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_lead_time_by_ship_mode(filtered), use_container_width=True)
with col2:
    st.plotly_chart(plot_ship_mode_region_heatmap(filtered), use_container_width=True)

st.divider()
st.subheader('Ship Mode × Region — Lead Time (days)')
pivot = filtered.groupby(['Ship Mode', 'Region'])['Shipping Lead Time'].mean().unstack().round(2)
st.dataframe(pivot, use_container_width=True)

st.subheader('Ship Mode × Region — Order Volume')
vol_pivot = filtered.groupby(['Ship Mode', 'Region']).size().unstack().fillna(0).astype(int)
st.dataframe(vol_pivot, use_container_width=True)