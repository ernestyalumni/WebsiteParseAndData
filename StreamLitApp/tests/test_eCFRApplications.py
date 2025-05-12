from StreamLitApp.app.eCFRApplications import get_count_for_agency_slugs

def test_get_count_for_agency_slugs():
    agency_slugs = [
        "administrative-conference-of-the-united-states",
        "advisory-council-on-historic-preservation",
        "special-inspector-general-for-afghanistan-reconstruction",
        "african-development-foundation"
    ]
    query = "federal register"
    results = get_count_for_agency_slugs(query, agency_slugs)

    print("results:", results)