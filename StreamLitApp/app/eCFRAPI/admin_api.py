import requests
import json

BASE_URL = "https://www.ecfr.gov/api/admin/v1"

def get_agencies():
    """
    Get all top-level agencies in name order with children also in name order.
    
    Returns:
        tuple: (status_code, is_expected_status_code,response_data)
    """
    url = f"{BASE_URL}/agencies.json"
    headers = {"accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        return response.status_code, True, response.json() \
            if response.status_code == 200 else None
    except Exception as e:
        return 500, False, {"error": str(e)}

def get_corrections(title=None, date=None, error_corrected_date=None):
    """
    Get all eCFR corrections, optionally filtered by title, date, or correction date.
    
    Args:
        title (str, optional): Title number (e.g., '1', '2', '50')
        date (str, optional): Date in YYYY-MM-DD format
        Corrections that occured on or before specified date and that were
        corrected on or after specified date.
        
        error_corrected_date (str, optional): Date in YYYY-MM-DD format
    
    Returns:
        tuple: (status_code, is_expected_status_code, response_data)
    """
    url = f"{BASE_URL}/corrections.json"
    headers = {"accept": "application/json"}
    params = {}
    
    if title:
        params['title'] = title
    if date:
        params['date'] = date
    if error_corrected_date:
        params['error_corrected_date'] = error_corrected_date
    
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.status_code, True, response.json() \
            if response.status_code == 200 else None
    except Exception as e:
        return 500, False, {"error": str(e)}

def get_corrections_by_title(title):
    """
    Get all corrections for a specific title.
    
    Args:
        title (str): Title number (e.g., '1', '2', '50')
    
    Returns:
        tuple: (status_code, is_expected_status_code, response_data)
    """
    url = f"{BASE_URL}/corrections/title/{title}.json"
    headers = {"accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        return response.status_code, True, response.json() \
            if response.status_code == 200 else None
    except Exception as e:
        return 500, False, {"error": str(e)}
