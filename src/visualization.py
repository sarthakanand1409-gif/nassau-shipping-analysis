import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_loader import US_STATE_COORDS


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
    monthly = df.groupby(pd.Grouper(key='Order Date', freq='ME'))['Shipping Lead Time'].mean().reset_index()
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


# US state name to abbreviation map (needed for choropleth)
STATE_ABBR = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'District Of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
    'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
    'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE',
    'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
    'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
    'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}


def plot_us_choropleth(state_perf, metric='Avg_Lead_Time'):
    """Choropleth map of US states colored by chosen metric."""
    df = state_perf.copy()
    df['State_Abbr'] = df['State/Province'].map(STATE_ABBR)
    df = df.dropna(subset=['State_Abbr'])

    fig = px.choropleth(
        df, locations='State_Abbr', locationmode='USA-states',
        color=metric, scope='usa',
        color_continuous_scale='RdYlGn_r' if metric == 'Avg_Lead_Time' else 'Blues',
        hover_name='State/Province',
        hover_data=['Volume', 'Avg_Lead_Time', 'Total_Sales'],
        title=f'US Map: {metric.replace("_", " ")} by State'
    )
    fig.update_layout(height=550)
    return fig


def plot_route_network_map(df, top_n=20):
    """Map showing factory → top N customer state routes as lines."""
    df = df.copy()

    # Add customer coordinates if missing
    if 'Customer Latitude' not in df.columns or 'Customer Longitude' not in df.columns:
        df['Customer Latitude'] = df['State/Province'].map(lambda s: US_STATE_COORDS.get(s, (None, None))[0])
        df['Customer Longitude'] = df['State/Province'].map(lambda s: US_STATE_COORDS.get(s, (None, None))[1])
        df = df.dropna(subset=['Customer Latitude', 'Customer Longitude'])

    # Top N routes by volume
    route_volume = df.groupby('Route_State').size().reset_index(name='Volume').nlargest(top_n, 'Volume')
    routes_to_plot = df[df['Route_State'].isin(route_volume['Route_State'])]
    
    # Aggregate per route to get one line per route
    route_summary = routes_to_plot.groupby(
        ['Factory', 'State/Province', 'Factory Latitude', 'Factory Longitude',
         'Customer Latitude', 'Customer Longitude']
    ).agg(
        Volume=('Order ID', 'count'),
        Avg_Lead_Time=('Shipping Lead Time', 'mean')
    ).reset_index()


    fig = go.Figure()

    # Plot route lines
    for _, row in route_summary.iterrows():
        fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            lon=[row['Factory Longitude'], row['Customer Longitude']],
            lat=[row['Factory Latitude'], row['Customer Latitude']],
            mode='lines',
            line=dict(width=max(1, row['Volume'] / 50), color='rgba(31, 119, 180, 0.5)'),
            opacity=0.6,
            hoverinfo='text',
            text=f"{row['Factory']} → {row['State/Province']}<br>Volume: {row['Volume']}<br>Avg LT: {row['Avg_Lead_Time']:.1f}d",
            showlegend=False
        ))

    # Plot factory markers
    factories = route_summary[['Factory', 'Factory Latitude', 'Factory Longitude']].drop_duplicates()
    fig.add_trace(go.Scattergeo(
        locationmode='USA-states',
        lon=factories['Factory Longitude'],
        lat=factories['Factory Latitude'],
        mode='markers+text',
        marker=dict(size=14, color='red', symbol='star'),
        text=factories['Factory'],
        textposition='top center',
        name='Factories'
    ))

    fig.update_layout(
        title=f'Top {top_n} Shipping Routes by Volume',
        geo=dict(scope='usa', projection_type='albers usa', showland=True, landcolor='rgb(243,243,243)'),
        height=600
    )
    return fig
