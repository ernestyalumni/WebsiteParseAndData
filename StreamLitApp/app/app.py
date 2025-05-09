"""
Usage:
(for development)
root@678c273b8639:/app/StreamLitApp# cd app/
root@678c273b8639:/app/StreamLitApp/app# streamlit run app.py 


"""

import streamlit as st
from components.header import create_header
from utils.data_loader import load_sample_data
import pages.overview
import pages.detailed_view
from pathlib import Path

# Get the directory where the current file is located
current_dir = Path(__file__).parent

# Page configuration
st.set_page_config(
    page_title="Data Visualization Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS using a path relative to the current file
css_path = current_dir / "assets" / "style.css"
try:
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning(f"CSS file not found at {css_path}. Using default styling.")

# Create header
create_header()

# Load data (this would be cached)
data = load_sample_data()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["Overview", "Detailed View"]
)

# Display selected page
if page == "Overview":
    pages.overview.show(data)
elif page == "Detailed View":
    pages.detailed_view.show(data)
