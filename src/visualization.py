import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def plot_lead_time_by_ship_mode(df):
    """Box plot of lead time by ship mode."""
    fig = px.box(
        df, x='Ship Mode', y='Shipping Lead Time',
        color='Ship Mode',
        title='Shipping Lead Time Distribution by Ship Mode',
        labels={'Shipping Lead Time': 'Lead Time (days)'}
    )
    fig.update_layout(showlegend=False, height=450)
    return fig


def plot_route_efficiency_leaderboard(route_kpi_df, n=15):
    """Horizontal bar chart of top N most efficient routes."""
    top = route_kpi_df.nsmallest(n, 'Avg_Lead_Time')
    fig = px.bar(
        top, x='Avg_Lead_Time', y='Route_State',
        orientation='h',
        color='Route_Efficiency_Score',
        color_continuous_scale='Greens',
        title=f'Top {n} Most Efficient Routes (by Avg Lead Time)',
        labels={'Avg_Lead_Time': 'Avg Lead Time (days)', 'Route_State': 'Route'}
    )
    fig.update_layout(height=600, yaxis={'categoryorder': 'total descending'})
    return fig


def plot_volume_vs_leadtime(state_perf):
    """Scatter: state volume vs lead time, colored by category."""
    fig = px.scatter(
        state_perf, x='Volume', y='Avg_Lead_Time',
        color='Performance_Category',
        size='Total_Sales',
        hover_data=['State/Province', 'Avg_Profit_Margin'],
        title='State Volume vs. Average Lead Time',
        labels={'Volume': 'Order Volume', 'Avg_Lead_Time': 'Avg Lead Time (days)'},
        color_discrete_map={
            'Critical Bottleneck': '#d62728',
            'Slow Route': '#ff7f0e',
            'High-Volume Healthy': '#2ca02c',
            'Standard': '#7f7f7f'
        }
    )
    fig.update_layout(height=500)
    return fig


def plot_lead_time_trend(df):
    """Monthly trend of avg lead time."""
    df = df.copy()
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    monthly = df.groupby(pd.Grouper(key='Order Date', freq='M'))['Shipping Lead Time'].mean().reset_index()
    fig = px.line(
        monthly, x='Order Date', y='Shipping Lead Time',
        title='Monthly Average Lead Time Trend',
        labels={'Shipping Lead Time': 'Avg Lead Time (days)'}
    )
    fig.update_layout(height=400)
    fig.update_traces(line_color='#1f77b4', line_width=3)
    return fig


def plot_factory_performance(df):
    """Bar chart: avg lead time by factory."""
    factory_perf = df.groupby('Factory').agg(
        Avg_Lead_Time=('Shipping Lead Time', 'mean'),
        Volume=('Order ID', 'count')
    ).reset_index().round(2)
    fig = px.bar(
        factory_perf, x='Factory', y='Avg_Lead_Time',
        color='Volume', color_continuous_scale='Blues',
        title='Average Lead Time by Factory',
        text='Avg_Lead_Time'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(height=450)
    return fig


def plot_ship_mode_region_heatmap(df):
    """Heatmap: ship mode × region average lead time."""
    pivot = df.groupby(['Ship Mode', 'Region'])['Shipping Lead Time'].mean().unstack().round(2)
    fig = px.imshow(
        pivot, text_auto=True, aspect='auto',
        color_continuous_scale='RdYlGn_r',
        title='Avg Lead Time: Ship Mode × Region (days)',
        labels={'color': 'Lead Time (days)'}
    )
    fig.update_layout(height=400)
    return fig