import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from visualization import (plot_route_efficiency_leaderboard,
                           plot_factory_performance, plot_lead_time_trend)
from kpi_calculator import compute_route_kpis

st.set_page_config(page_title='Route Overview', layout='wide')
st.title('🛣️ Route Performance Overview')

if 'filtered_df' not in st.session_state:
    st.warning('Please go to the Home page first to set filters.')
    st.stop()

filtered = st.session_state['filtered_df']
delay_threshold = st.session_state['delay_threshold']

if len(filtered) == 0:
    st.error('No data matches the current filters. Adjust filters and retry.')
    st.stop()

# Recompute KPIs on filtered data
route_kpis_filt = compute_route_kpis(filtered, 'Route_State', delay_threshold)

# Top N selector
n_routes = st.slider('Number of routes to display', 5, 30, 15)

col1, col2 = st.columns(2)
with col1:
    st.subheader('🏆 Most Efficient Routes')
    top = route_kpis_filt[route_kpis_filt['Route_Volume'] >= 10].nsmallest(n_routes, 'Avg_Lead_Time')
    st.dataframe(
        top[['Route_State', 'Avg_Lead_Time', 'Route_Volume', 'Delay_Frequency_%', 'Route_Efficiency_Score']],
        use_container_width=True, hide_index=True
    )
with col2:
    st.subheader('⚠️ Least Efficient Routes')
    bottom = route_kpis_filt[route_kpis_filt['Route_Volume'] >= 10].nlargest(n_routes, 'Avg_Lead_Time')
    st.dataframe(
        bottom[['Route_State', 'Avg_Lead_Time', 'Route_Volume', 'Delay_Frequency_%', 'Route_Efficiency_Score']],
        use_container_width=True, hide_index=True
    )

st.divider()
st.plotly_chart(plot_route_efficiency_leaderboard(route_kpis_filt, n=n_routes), use_container_width=True)

st.divider()
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_factory_performance(filtered), use_container_width=True)
with col2:
    st.plotly_chart(plot_lead_time_trend(filtered), use_container_width=True)
