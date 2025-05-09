import streamlit as st
import pandas as pd
import plotly.express as px
from components.charts import time_series_chart

def show(data):
    """Display detailed view with interactive filters"""
    st.header("Detailed Analysis")
    
    # Convert date column to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(data['date']):
        data['date'] = pd.to_datetime(data['date'])
    
    # Filters
    st.sidebar.subheader("Filters")
    
    # Date range filter
    date_min = data['date'].min().date()
    date_max = data['date'].max().date()
    
    start_date, end_date = st.sidebar.date_input(
        "Date Range",
        [date_min, date_max],
        min_value=date_min,
        max_value=date_max
    )
    
    # Category filter
    categories = ['All'] + sorted(data['category'].unique().tolist())
    selected_category = st.sidebar.selectbox("Category", categories)
    
    # Apply filters
    filtered_data = data.copy()
    
    # Date filter
    filtered_data = filtered_data[
        (filtered_data['date'].dt.date >= start_date) & 
        (filtered_data['date'].dt.date <= end_date)
    ]
    
    # Category filter
    if selected_category != 'All':
        filtered_data = filtered_data[filtered_data['category'] == selected_category]
    
    # Show filtered data info
    st.info(f"Showing {len(filtered_data)} records")
    
    # Interactive charts
    st.subheader("Metrics Over Time")
    
    # Metric selector
    metric = st.selectbox(
        "Select metric to visualize",
        ["value", "metric1", "metric2"]
    )
    
    # Display time series
    time_series_chart(filtered_data, 'date', metric, f"{metric.title()} Over Time")
    
    # Correlation heatmap
    st.subheader("Correlation Between Metrics")
    
    corr = filtered_data[['value', 'metric1', 'metric2']].corr()
    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        title="Correlation Heatmap"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Raw data table
    st.subheader("Raw Data")
    st.dataframe(filtered_data, use_container_width=True)
