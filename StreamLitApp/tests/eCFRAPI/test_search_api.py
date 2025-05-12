"""
USAGE:
pytest StreamLitApp/tests/eCFRAPI/test_search_api.py -v
"""

# Import the function to test
from StreamLitApp.app.eCFRAPI.search_api import (
    get_results,
    get_count,
    get_summary,
    get_counts_daily,
    get_counts_titles,
)

from StreamLitApp.app.eCFRAPI.admin_api import get_agencies

def test_get_count():
    query="President*"
    agency_slugs=[
        "foreign-service-grievance-board",
        "government-ethics-office",
        "office-of-administration-for-children-and-families-family-assistance-(assistance-programs)"]

    status_code, is_expected_status_code, response_data = get_count(
        query=query,
        agency_slugs=agency_slugs
    )
    assert is_expected_status_code
    assert status_code == 200
    print("response_data: ", response_data)

    expected_keys_0 = ["meta"]
    expected_keys_1 = [
        "total_count",
        "description"
    ]
    assert all(key in response_data for key in expected_keys_0)
    assert all(key in response_data["meta"] for key in expected_keys_1)

def test_get_count_for_each_agency():
    status_code, is_expected_status_code, response_data = get_agencies()
    assert is_expected_status_code

    result = []

    query = "Congress*"

    # TODO: This is slow to get all.
    # for agency in response_data["agencies"]:
    #     agency_slug = agency["slug"]
    #     _, is_expected_status_code, response_data = get_count(
    #         query=query,
    #         agency_slugs=[agency_slug]
    #     )
    #     assert is_expected_status_code
    #     result.append({
    #         "agency_slug": agency_slug,
    #         "count": response_data["meta"]["total_count"]
    #     })

    # print("result: ", result)

def test_get_counts_titles_by_title():
    query="President*"
    status_code, is_expected_status_code, response_data = get_counts_titles(
        query=query
    )

    assert is_expected_status_code
    assert status_code == 200
    print("response_data: ", response_data)
