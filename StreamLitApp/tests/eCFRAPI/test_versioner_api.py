"""
USAGE:
pytest StreamLitApp/tests/eCFRAPI/test_versioner_api.py -v
"""

# Import the function to test
from StreamLitApp.app.eCFRAPI.versioner_api import (
    get_structure,
    get_titles
)

def test_get_structure_with_recent_date():
    date="2025-05-01"
    title="1"
    status_code, is_expected_status_code, response_data = get_structure(
        date=date,
        title=title
    )

    assert is_expected_status_code
    assert status_code == 200
    print("response_data: ", response_data)

    print("response_data.keys(): ", response_data.keys())
    print("len(response_data['children']): ", len(response_data["children"]))

def test_get_titles():
    status_code, is_expected_status_code, response_data = get_titles()

    assert is_expected_status_code
    assert status_code == 200
    print("response_data: ", response_data)

    print("response_data.keys(): ", response_data.keys())
    for title in response_data["titles"]:
        print("number: ", title["number"])
        print("name: ", title["name"])