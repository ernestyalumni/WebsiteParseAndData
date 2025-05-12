from StreamLitApp.app.eCFRAPI.admin_api import (
    get_agencies
)

from StreamLitApp.app.ParseeCFR.parse_admin_api import (
    get_all_abridged_agencies,
    get_title_and_chapter_from_agency
)

def test_get_all_abridged_agencies():
    status_code, is_expected_status_code, response_data = get_agencies()
    assert is_expected_status_code
    assert status_code == 200
    assert set(response_data.keys()) == set({"agencies"})

    expected_agency_keys = set(['name', 'short_name', 'display_name', 'sortable_name', 'slug', 'children', 'cfr_references'])

    assert set(response_data["agencies"][0].keys()) == expected_agency_keys

    list_of_agencies = get_all_abridged_agencies(response_data)
    assert len(list_of_agencies) == 153

    for agency in list_of_agencies:
        print("agency:", agency)

def test_get_all_abridged_agencies_can_get_all_slugs():
    _, is_expected_status_code, response_data = get_agencies()
    assert is_expected_status_code
    list_of_agencies = get_all_abridged_agencies(response_data)

    for agency in list_of_agencies:
        print("agency:", agency["name"])
        print("agency slug:", agency["slug"])


def test_get_title_and_chapter_from_agency():
    status_code, is_expected_status_code, response_data = get_agencies()
    assert is_expected_status_code

    title_and_chapter = get_title_and_chapter_from_agency(
        response_data, name="Federal Travel Regulation System")
    print(title_and_chapter)