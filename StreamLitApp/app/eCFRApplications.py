from StreamLitApp.app.eCFRAPI.search_api import get_count

def get_count_for_agency_slugs(query, agency_slugs):
    results = []

    for agency_slug in agency_slugs:
        data = {}

        _, is_expected_status_code, response_data = get_count(
            query=query,
            agency_slugs=[agency_slug])
        if not is_expected_status_code:
            raise Exception(
                f"Error getting count for agency slug: {agency_slug}")
        data["agency_slug"] = agency_slug
        data["total_count"] = response_data["meta"]["total_count"]
        results.append(data)
    return results