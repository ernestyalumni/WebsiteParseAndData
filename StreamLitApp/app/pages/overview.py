import streamlit as st
import pandas as pd
from components.charts import time_series_chart, bar_chart, pie_chart

def show(data):
    """Display overview dashboard"""
    st.header("Overview Dashboard")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", f"{len(data):,}")
    with col2:
        st.metric("Average Value", f"{data['value'].mean():.2f}")
    with col3:
        st.metric("Categories", data['category'].nunique())
    
    # Time series chart
    st.subheader("Value Over Time")
    time_series_chart(data, 'date', 'value', "Value Trend")
    
    # Two charts side by side
    col1, col2 = st.columns(2)
    
    with col1:
        # Category distribution
        category_counts = data['category'].value_counts().reset_index()
        category_counts.columns = ['category', 'count']
        bar_chart(category_counts, 'category', 'count', "Category Distribution")
    
    with col2:
        # Pie chart
        pie_chart(data, 'category', 'value', "Value by Category")
