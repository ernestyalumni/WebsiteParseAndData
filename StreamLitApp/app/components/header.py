import streamlit as st

def create_header():
    """Create a header for the dashboard"""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=100)
    
    with col2:
        st.title("Data Visualization Dashboard")
        st.markdown("Interactive dashboard for exploring and visualizing data")
