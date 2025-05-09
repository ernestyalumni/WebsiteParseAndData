import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def time_series_chart(data, x_col, y_col, title="Time Series"):
    """Create a time series chart"""
    fig = px.line(
        data, 
        x=x_col, 
        y=y_col,
        title=title,
        template="plotly_white"
    )
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        height=400
    )
    
    return st.plotly_chart(fig, use_container_width=True)

def bar_chart(data, x_col, y_col, title="Bar Chart"):
    """Create a bar chart"""
    fig = px.bar(
        data, 
        x=x_col, 
        y=y_col,
        title=title,
        template="plotly_white"
    )
    
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        height=400
    )
    
    return st.plotly_chart(fig, use_container_width=True)

def pie_chart(data, names_col, values_col, title="Distribution"):
    """Create a pie chart"""
    # Group data if needed
    if len(data) > 10:  # If too many rows, aggregate
        plot_data = data.groupby(names_col)[values_col].sum().reset_index()
    else:
        plot_data = data
        
    fig = px.pie(
        plot_data, 
        names=names_col, 
        values=values_col,
        title=title
    )
    
    fig.update_layout(height=400)
    
    return st.plotly_chart(fig, use_container_width=True)
