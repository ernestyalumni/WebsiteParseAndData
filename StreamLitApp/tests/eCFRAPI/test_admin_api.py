"""
USAGE:
pytest StreamLitApp/tests/eCFRAPI/test_admin_api.py -v
"""

import pytest
import json
from unittest.mock import patch, MagicMock

# Import the function to test
from StreamLitApp.app.eCFRAPI.admin_api import (
    get_agencies,
    get_corrections,
    get_corrections_by_title
)

def test_get_agencies_live():
    """
    Test the get_agencies function with a live API call.
    This test will be skipped by default to avoid unnecessary API calls during
    testing.
    """
    # Skip this test by default to avoid making actual API calls during testing
    pytest.skip("Skipping live API test to avoid unnecessary API calls")
    
    # Make the actual API call
    status_code, response_data = get_agencies()
    
    # Print the response for inspection
    print(f"Status Code: {status_code}")
    if response_data:
        # Pretty print the first agency for readability
        print("\nFirst agency in response:")
        first_agency = response_data.get('agencies', [])[0] \
            if response_data.get('agencies') else None
        if first_agency:
            print(json.dumps(first_agency, indent=2))
        
        # Print total number of agencies
        agencies_count = len(response_data.get('agencies', []))
        print(f"\nTotal agencies: {agencies_count}")
    
    # Basic assertions
    assert status_code == 200
    assert response_data is not None
    assert 'agencies' in response_data
    assert isinstance(response_data['agencies'], list)
    assert len(response_data['agencies']) > 0

@patch('StreamLitApp.app.eCFRAPI.admin_api.requests.get')
def test_get_agencies_mock(mock_get):
    """
    Test the get_agencies function with a mocked API response.
    """
    # Create a mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'agencies': [
            {
                'name': 'Department of Agriculture',
                'short_name': 'USDA',
                'display_name': 'Department of Agriculture',
                'sortable_name': 'Agriculture, Department of',
                'slug': 'agriculture-department',
                'children': [],
                'cfr_references': [
                    {
                        'title': 7,
                        'chapter': 'I'
                    }
                ]
            }
        ]
    }
    
    # Set up the mock
    mock_get.return_value = mock_response
    
    # Call the function
    status_code, is_expected_status_code, response_data = get_agencies()

    assert is_expected_status_code
    
    # Print the mocked response
    print(f"Status Code: {status_code}")
    if response_data:
        print("\nMocked response data:")
        print(json.dumps(response_data, indent=2))
    
    # Assertions
    assert status_code == 200
    assert response_data is not None
    assert 'agencies' in response_data
    assert isinstance(response_data['agencies'], list)
    assert len(response_data['agencies']) > 0
    assert response_data['agencies'][0]['name'] == 'Department of Agriculture'
    
    # Verify the mock was called correctly
    mock_get.assert_called_once_with(
        "https://www.ecfr.gov/api/admin/v1/agencies.json",
        headers={"accept": "application/json"}
    )

def test_get_agencies_error_handling():
    """
    Test error handling in the get_agencies function.
    """
    # Use a non-existent URL to force an error
    with patch(
        'StreamLitApp.app.eCFRAPI.admin_api.BASE_URL',
        'https://nonexistent-url'):
        status_code, is_expected_status_code, response_data = get_agencies()

        assert not is_expected_status_code
        # Print the error response
        print(f"Error Status Code: {status_code}")
        print(f"Error Response: {response_data}")
        
        # Assertions for error case
        assert status_code == 500
        assert response_data is not None
        assert 'error' in response_data

def test_get_agencies():
    status_code, is_expected_status_code, response_data = get_agencies()

    assert is_expected_status_code
    # Print the response for inspection
    print(f"Status Code: {status_code}")
    if response_data:
        # Pretty print the first agency for readability
        print("\nFirst agency in response:")
        first_agency = response_data.get('agencies', [])[0] \
            if response_data.get('agencies') else None
        if first_agency:
            print(json.dumps(first_agency, indent=2))
        
        # Print total number of agencies
        agencies_count = len(response_data.get('agencies', []))
        print(f"\nTotal agencies: {agencies_count}")
    
        print("response_data: ", response_data)

def test_get_agencies_gets_children():
    status_code, is_expected_status_code, response_data = get_agencies()

    assert is_expected_status_code
    # Print the response for inspection
    print(f"Status Code: {status_code}")
    if response_data:
        for agency in response_data["agencies"]:
            print("agency name: ", agency["name"])
            print("agency sortable_name: ", agency["sortable_name"])
            print("agency slug: ", agency["slug"])
            if agency["children"] == []:
                print("agency children: ", agency["children"])
            else:
                for child in agency["children"]:
                    print("child: ", child)


def test_get_corrections_with_title():
    status_code, is_expected_status_code, response_data = \
        get_corrections(title='2')
    print("status_code: ", status_code)
    print("is_expected_status_code: ", is_expected_status_code)
    print("response_data: ", response_data)

def test_get_corrections_with_title_and_date():
    status_code, is_expected_status_code, response_data = \
        get_corrections(title='2', date='2013-02-22')
    print("status_code: ", status_code)
    print("is_expected_status_code: ", is_expected_status_code)
    print("response_data: ", response_data)
    assert len(response_data['ecfr_corrections']) == 1

def test_get_corrections_by_title():
    status_code, is_expected_status_code, response_data = \
        get_corrections_by_title('2')
    print("status_code: ", status_code)
    print("is_expected_status_code: ", is_expected_status_code)
    print("response_data: ", response_data)
