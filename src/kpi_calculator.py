"""
Compute route-level KPIs as defined in the project spec.
"""
import os
import pandas as pd
import numpy as np


def compute_route_kpis(df, route_col='Route_State', delay_threshold_days=7):
    """
    Aggregate shipment-level data into route-level KPIs.

    KPIs:
    - Average Lead Time
    - Lead Time Std Dev (variability)
    - Route Volume (number of orders)
    - Delay Frequency (% > threshold)
    - Route Efficiency Score (normalized inverse lead time)
    - Total Sales, Total Units, Total Gross Profit
    """
    agg = df.groupby(route_col).agg(
        Avg_Lead_Time=('Shipping Lead Time', 'mean'),
        Median_Lead_Time=('Shipping Lead Time', 'median'),
        Lead_Time_Std=('Shipping Lead Time', 'std'),
        Route_Volume=('Order ID', 'count'),
        Total_Sales=('Sales', 'sum'),
        Total_Units=('Units', 'sum'),
        Total_Gross_Profit=('Gross Profit', 'sum'),
        Avg_Profit_Margin=('Profit Margin %', 'mean')
    ).reset_index()

    # Delay frequency: % of shipments exceeding threshold per route
    delay_freq = (
        df.assign(is_delayed=lambda x: x['Shipping Lead Time'] > delay_threshold_days)
          .groupby(route_col)['is_delayed']
          .mean()
          .reset_index()
          .rename(columns={'is_delayed': 'Delay_Frequency_%'})
    )
    delay_freq['Delay_Frequency_%'] = (delay_freq['Delay_Frequency_%'] * 100).round(2)
    agg = agg.merge(delay_freq, on=route_col)

    # Route Efficiency Score: lower lead time = higher score; normalize 0–100
    max_lt = agg['Avg_Lead_Time'].max()
    min_lt = agg['Avg_Lead_Time'].min()
    if max_lt > min_lt:
        agg['Route_Efficiency_Score'] = (
            (max_lt - agg['Avg_Lead_Time']) / (max_lt - min_lt) * 100
        ).round(2)
    else:
        agg['Route_Efficiency_Score'] = 100.0

    # Round numeric columns
    for col in ['Avg_Lead_Time', 'Median_Lead_Time', 'Lead_Time_Std', 'Avg_Profit_Margin']:
        agg[col] = agg[col].round(2)

    return agg.sort_values('Route_Volume', ascending=False)


def top_bottom_routes(route_kpi_df, n=10, min_volume=10):
    """Return top-N most efficient and bottom-N least efficient routes."""
    qualified = route_kpi_df[route_kpi_df['Route_Volume'] >= min_volume].copy()
    top = qualified.nsmallest(n, 'Avg_Lead_Time')
    bottom = qualified.nlargest(n, 'Avg_Lead_Time')
    return top, bottom


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data', 'Processed')
    df = pd.read_csv(os.path.join(data_dir, 'cleaned_data.csv'))

    # Compute route-state KPIs
    route_state_kpis = compute_route_kpis(df, 'Route_State')
    route_state_kpis.to_csv(os.path.join(data_dir, 'route_state_kpis.csv'), index=False)
    print(f"✓ Route-state KPIs: {len(route_state_kpis)} routes")
    print(route_state_kpis.head(10))

    # Compute route-region KPIs
    route_region_kpis = compute_route_kpis(df, 'Route_Region')
    route_region_kpis.to_csv(os.path.join(data_dir, 'route_region_kpis.csv'), index=False)
    print(f"\n✓ Route-region KPIs: {len(route_region_kpis)} routes")

    # Top/bottom routes
    top, bottom = top_bottom_routes(route_state_kpis, n=10)
    print(f"\nTop 10 most efficient routes:")
    print(top[['Route_State', 'Avg_Lead_Time', 'Route_Volume', 'Route_Efficiency_Score']])
    print(f"\nBottom 10 least efficient routes:")
    print(bottom[['Route_State', 'Avg_Lead_Time', 'Route_Volume', 'Route_Efficiency_Score']])