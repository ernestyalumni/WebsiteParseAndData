import streamlit as st
import pandas as pd
from components.charts import time_series_chart, bar_chart, pie_chart
from utils.ecfr_service import ECFRService

def show(data):
    """Display overview dashboard"""
    st.header("eCFR Analyzer Dashboard")
    
    # Initialize eCFR service
    ecfr_service = ECFRService()
    
    # Add a section for eCFR Titles
    st.subheader("Federal Regulation Titles")
    
    # Fetch titles from Supabase
    titles = ecfr_service.fetch_titles()
    
    if not titles.empty:
        # Display the number of titles
        st.metric("Total CFR Titles", f"{len(titles)}")
        
        # Display titles in a dataframe
        st.dataframe(
            titles[['number', 'name']].rename(columns={'number': 'Title Number', 'name': 'Title Name'}),
            use_container_width=True
        )
        
        # Create a selectbox for exploring titles
        title_options = [f"{row['number']} - {row['name']}" for _, row in titles.iterrows()]
        selected_title = st.selectbox("Select a Title to Explore", [""] + title_options)
        
        if selected_title:
            # Extract title number and name
            title_parts = selected_title.split(" - ", 1)
            title_number = title_parts[0]
            title_name = title_parts[1] if len(title_parts) > 1 else ""
            
            st.write(f"### Title {title_number}: {title_name}")
            st.write("In a full implementation, this would show parts and sections of this title.")
    else:
        st.info("No title data available in Supabase.")
        
        # Add a button to add test data
        if st.button("Add Test Data to Supabase"):
            with st.spinner("Adding test data to Supabase..."):
                success = ecfr_service.add_test_titles()
                if success:
                    st.success("Test data added successfully! Refresh to see the data.")
                    st.experimental_rerun()
                else:
                    st.error("Failed to add test data. Check the logs for details.")
    
    # Original dashboard content
    st.subheader("Sample Data Visualization")
    
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
