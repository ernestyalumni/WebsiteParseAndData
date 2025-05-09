import pandas as pd
import streamlit as st
from pathlib import Path

# Get the app directory (parent of utils)
app_dir = Path(__file__).parent.parent

# Use app_dir to create absolute paths
data_dir = app_dir / "data"
data_dir.mkdir(exist_ok=True)

# Use absolute path for CSV
csv_path = data_dir / "sample_data.csv"

@st.cache_data
def load_sample_data():
    """Load and cache sample data"""
    try:
        # Try to load from data directory
        # Parse dates when reading the CSV
        return pd.read_csv(csv_path, parse_dates=['date'])
    except FileNotFoundError:
        # If file doesn't exist, create sample data
        import numpy as np
        
        # Create sample time series data
        dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
        values = np.cumsum(np.random.randn(100)) + 100  # Random walk
        
        # Create sample categorical data
        categories = ['Category A', 'Category B', 'Category C', 'Category D']
        category_data = np.random.choice(categories, size=100)
        
        # Create DataFrame
        df = pd.DataFrame({
            'date': dates,
            'value': values,
            'category': category_data,
            'metric1': np.random.randn(100) * 10 + 50,
            'metric2': np.random.randn(100) * 5 + 25
        })
        
        # Save for future use
        df.to_csv(csv_path, index=False)
        return df
