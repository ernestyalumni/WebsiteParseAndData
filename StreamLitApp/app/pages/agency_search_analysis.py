import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from StreamLitApp.app.eCFRAPI.admin_api import get_agencies
from StreamLitApp.app.ParseeCFR.parse_admin_api import get_all_abridged_agencies
from StreamLitApp.app.eCFRApplications import get_count_for_agency_slugs

def get_all_agency_slugs():
    """Get all agency slugs from the eCFR API"""
    status_code, is_expected_status_code, response_data = get_agencies()
    
    if not is_expected_status_code:
        st.error(f"Failed to fetch agencies: Status code {status_code}")
        return []
    
    list_of_agencies = get_all_abridged_agencies(response_data)
    list_of_agency_slugs = []
    for agency in list_of_agencies:
        list_of_agency_slugs.append(
            {"name": agency["name"], "slug": agency["slug"]})

    return list_of_agency_slugs

def run_agency_search_analysis():
    st.title("eCFR Agency Search Analysis")
    
    # Query input
    query = st.text_input("Enter search query (e.g., 'Congress*', 'President*')", 
                         help="Use * for wildcard searches")
    
    # Get all agencies
    agencies = get_all_agency_slugs()
    
    # Create a DataFrame for easier handling
    agencies_df = pd.DataFrame(agencies)
    
    # Display agencies with multiselect
    st.subheader("Select Agencies")
    
    # Create columns for better layout
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Add select all/none buttons
        if st.button("Select All (this takes a while)"):
            st.session_state.selected_agencies = agencies_df['slug'].tolist()
        if st.button("Clear Selection"):
            st.session_state.selected_agencies = []
    
    # Initialize session state for selected agencies if not exists
    if 'selected_agencies' not in st.session_state:
        st.session_state.selected_agencies = []
    
    # Create a multiselect widget with agency names and store slugs
    selected_agency_names = st.multiselect(
        "Select agencies to analyze:",
        options=agencies_df['name'].tolist(),
        default=[],
        format_func=lambda x: x,
        key="agency_multiselect"
    )
    
    # Update session state based on selection
    selected_slugs = agencies_df[agencies_df['name'].isin(selected_agency_names)]['slug'].tolist()
    st.session_state.selected_agencies = selected_slugs
    
    # Show the number of selected agencies
    st.write(f"Selected {len(st.session_state.selected_agencies)} agencies")
    
    # Run analysis button
    if st.button("Run Analysis", disabled=(not query or len(st.session_state.selected_agencies) == 0)):
        if not query:
            st.error("Please enter a search query")
        elif len(st.session_state.selected_agencies) == 0:
            st.error("Please select at least one agency")
        else:
            with st.spinner("Analyzing data..."):
                try:
                    # Get count data for selected agencies
                    results = get_count_for_agency_slugs(query, st.session_state.selected_agencies)
                    
                    # Convert to DataFrame
                    results_df = pd.DataFrame(results)
                    
                    # Map slugs back to agency names for better readability
                    slug_to_name = dict(zip(agencies_df['slug'], agencies_df['name']))
                    results_df['agency_name'] = results_df['agency_slug'].map(slug_to_name)
                    
                    # Sort by count for better visualization
                    results_df = results_df.sort_values('total_count', ascending=False)
                    
                    # Display results
                    st.subheader(f"Search Results for '{query}'")
                    st.dataframe(results_df[['agency_name', 'total_count']])
                    
                    # Create histogram
                    st.subheader("Results Visualization")
                    
                    fig, ax = plt.subplots(figsize=(12, 8))
                    
                    # Use seaborn for better styling
                    sns.barplot(x='total_count', y='agency_name', data=results_df, ax=ax)
                    
                    ax.set_title(f"Count of '{query}' Mentions by Agency")
                    ax.set_xlabel("Count")
                    ax.set_ylabel("Agency")
                    
                    # Adjust layout
                    plt.tight_layout()
                    
                    # Display the plot
                    st.pyplot(fig)
                    
                    # Add download button for the data
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name=f"ecfr_search_{query.replace('*', '')}.csv",
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    run_agency_search_analysis()
