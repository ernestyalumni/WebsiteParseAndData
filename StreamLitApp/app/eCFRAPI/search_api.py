import requests

BASE_URL = "https://www.ecfr.gov/api/search/v1"

def get_results(
    query,
    agency_slugs=None,
    date=None,
    last_modified_after=None,
    last_modified_on_or_after=None,
    last_modified_before=None,
    last_modified_on_or_before=None,
    per_page=None,
    page=None,
    order=None,
    paginate_by=None,
):
    """
    Search the eCFR for the given query with comprehensive parameter support.
    
    Args:
        query (str): Search term; searches the headings and the full text
        agency_slugs (list, optional): List of agency slugs to limit content
        date (str, optional): Limit to content present on this date (YYYY-MM-DD)
        last_modified_after (str, optional): Limit to content last modified after this date (YYYY-MM-DD)
        last_modified_on_or_after (str, optional): Limit to content last modified on or after this date (YYYY-MM-DD)
        last_modified_before (str, optional): Limit to content last modified before this date (YYYY-MM-DD)
        last_modified_on_or_before (str, optional): Limit to content last modified on or before this date (YYYY-MM-DD)
        per_page (int, optional): Number of results per page; max of 1,000
        page (int, optional): Page of results; can't paginate beyond 10,000 total results
        order (str, optional): Order of results
        paginate_by (str, optional): How results should be paginated - 'date' will group results
                                    so that all results from a date appear on the same page
    
    Returns:
        tuple: (status_code, is_expected_status_code, response_data)
    """
    url = f"{BASE_URL}/results"
    headers = {"accept": "application/json"}
    
    # Build parameters dictionary
    params = {"query": query}
    
    # Add optional parameters if provided
    if agency_slugs:
        params["agency_slugs[]"] = agency_slugs
    if date:
        params["date"] = date
    if last_modified_after:
        params["last_modified_after"] = last_modified_after
    if last_modified_on_or_after:
        params["last_modified_on_or_after"] = last_modified_on_or_after
    if last_modified_before:
        params["last_modified_before"] = last_modified_before
    if last_modified_on_or_before:
        params["last_modified_on_or_before"] = last_modified_on_or_before
    if per_page:
        params["per_page"] = per_page
    if page:
        params["page"] = page
    if order:
        params["order"] = order
    if paginate_by:
        params["paginate_by"] = paginate_by

    try:
        response = requests.get(url, headers=headers, params=params)
        return \
            response.status_code, \
            response.status_code == 200, \
            response.json() if response.status_code == 200 else None
    except Exception as e:
        return 500, False, {"error": str(e)}

def get_count(
    query,
    agency_slugs=None,
    date=None,
    last_modified_after=None,
    last_modified_on_or_after=None,
    last_modified_before=None,
    last_modified_on_or_before=None,
):
    """
    Get the count of search results for the given query.
    
    Args:
        query (str): Search term; searches the headings and the full text
        agency_slugs (list, optional): List of agency slugs to limit content
        date (str, optional): Limit to content present on this date (YYYY-MM-DD)
        last_modified_after (str, optional): Limit to content last modified after this date (YYYY-MM-DD)
        last_modified_on_or_after (str, optional): Limit to content last modified on or after this date (YYYY-MM-DD)
        last_modified_before (str, optional): Limit to content last modified before this date (YYYY-MM-DD)
        last_modified_on_or_before (str, optional): Limit to content last modified on or before this date (YYYY-MM-DD)
    
    Returns:
        tuple: (status_code, is_expected_status_code, response_data)
    """
    url = f"{BASE_URL}/count"
    headers = {"accept": "application/json"}
    
    # Build parameters dictionary
    params = {"query": query}
    
    # Add optional parameters if provided
    if agency_slugs:
        params["agency_slugs[]"] = agency_slugs
    if date:
        params["date"] = date
    if last_modified_after:
        params["last_modified_after"] = last_modified_after
    if last_modified_on_or_after:
        params["last_modified_on_or_after"] = last_modified_on_or_after
    if last_modified_before:
        params["last_modified_before"] = last_modified_before
    if last_modified_on_or_before:
        params["last_modified_on_or_before"] = last_modified_on_or_before
    
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.status_code, response.status_code == 200, response.json() if response.status_code == 200 else None
    except Exception as e:
        return 500, False, {"error": str(e)}

def get_summary(
    query,
    agency_slugs=None,
    date=None,
    last_modified_after=None,
    last_modified_on_or_after=None,
    last_modified_before=None,
    last_modified_on_or_before=None,
):
    """
    Get summary details for search results.
    
    Args:
        query (str): Search term; searches the headings and the full text
        agency_slugs (list, optional): List of agency slugs to limit content
        date (str, optional): Limit to content present on this date (YYYY-MM-DD)
        last_modified_after (str, optional): Limit to content last modified after this date (YYYY-MM-DD)
        last_modified_on_or_after (str, optional): Limit to content last modified on or after this date (YYYY-MM-DD)
        last_modified_before (str, optional): Limit to content last modified before this date (YYYY-MM-DD)
        last_modified_on_or_before (str, optional): Limit to content last modified on or before this date (YYYY-MM-DD)
    
    Returns:
        tuple: (status_code, is_expected_status_code, response_data)
    """
    url = f"{BASE_URL}/summary"
    headers = {"accept": "application/json"}
    
    # Build parameters dictionary
    params = {"query": query}
    
    # Add optional parameters if provided
    if agency_slugs:
        params["agency_slugs[]"] = agency_slugs
    if date:
        params["date"] = date
    if last_modified_after:
        params["last_modified_after"] = last_modified_after
    if last_modified_on_or_after:
        params["last_modified_on_or_after"] = last_modified_on_or_after
    if last_modified_before:
        params["last_modified_before"] = last_modified_before
    if last_modified_on_or_before:
        params["last_modified_on_or_before"] = last_modified_on_or_before
    
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.status_code, response.status_code == 200, response.json() \
            if response.status_code == 200 else None
    except Exception as e:
        return 500, False, {"error": str(e)}

def get_counts_daily(
    query,
    agency_slugs=None,
    date=None,
    last_modified_after=None,
    last_modified_on_or_after=None,
    last_modified_before=None,
    last_modified_on_or_before=None,
):
    """
    Get search result counts by date.
    
    Args:
        query (str): Search term; searches the headings and the full text
        agency_slugs (list, optional): List of agency slugs to limit content
        date (str, optional): Limit to content present on this date (YYYY-MM-DD)
        last_modified_after (str, optional): Limit to content last modified after this date (YYYY-MM-DD)
        last_modified_on_or_after (str, optional): Limit to content last modified on or after this date (YYYY-MM-DD)
        last_modified_before (str, optional): Limit to content last modified before this date (YYYY-MM-DD)
        last_modified_on_or_before (str, optional): Limit to content last modified on or before this date (YYYY-MM-DD)
    
    Returns:
        tuple: (status_code, is_expected_status_code, response_data)
    """
    url = f"{BASE_URL}/counts/daily"
    headers = {"accept": "application/json"}
    
    # Build parameters dictionary
    params = {"query": query}
    
    # Add optional parameters if provided
    if agency_slugs:
        params["agency_slugs[]"] = agency_slugs
    if date:
        params["date"] = date
    if last_modified_after:
        params["last_modified_after"] = last_modified_after
    if last_modified_on_or_after:
        params["last_modified_on_or_after"] = last_modified_on_or_after
    if last_modified_before:
        params["last_modified_before"] = last_modified_before
    if last_modified_on_or_before:
        params["last_modified_on_or_before"] = last_modified_on_or_before
   
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.status_code, response.status_code == 200, response.json() \
            if response.status_code == 200 else None
    except Exception as e:
        return 500, False, {"error": str(e)}

def get_counts_titles(
    query,
    agency_slugs=None,
    date=None,
    last_modified_after=None,
    last_modified_on_or_after=None,
    last_modified_before=None,
    last_modified_on_or_before=None
):
    """
    Get search result counts by title.
    
    Args:
        query (str): Search term; searches the headings and the full text
        agency_slugs (list, optional): List of agency slugs to limit content
        date (str, optional): Limit to content present on this date (YYYY-MM-DD)
        last_modified_after (str, optional): Limit to content last modified after this date (YYYY-MM-DD)
        last_modified_on_or_after (str, optional): Limit to content last modified on or after this date (YYYY-MM-DD)
        last_modified_before (str, optional): Limit to content last modified before this date (YYYY-MM-DD)
        last_modified_on_or_before (str, optional): Limit to content last modified on or before this date (YYYY-MM-DD)
    
    Returns:
        tuple: (status_code, is_expected_status_code, response_data)
    """
    url = f"{BASE_URL}/counts/titles"
    headers = {"accept": "application/json"}
    
    # Build parameters dictionary
    params = {"query": query}
    
    # Add optional parameters if provided
    if agency_slugs:
        params["agency_slugs[]"] = agency_slugs
    if date:
        params["date"] = date
    if last_modified_after:
        params["last_modified_after"] = last_modified_after
    if last_modified_on_or_after:
        params["last_modified_on_or_after"] = last_modified_on_or_after
    if last_modified_before:
        params["last_modified_before"] = last_modified_before
    if last_modified_on_or_before:
        params["last_modified_on_or_before"] = last_modified_on_or_before
    
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.status_code, response.status_code == 200, response.json() \
            if response.status_code == 200 else None
    except Exception as e:
        return 500, False, {"error": str(e)}

