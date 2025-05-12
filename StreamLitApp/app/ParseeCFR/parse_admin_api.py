def get_all_abridged_agencies(json_response):
    list_of_agencies = []
    for agency in json_response["agencies"]:
        data = {}
        data["name"] = agency["name"]
        data["short_name"] = agency["short_name"]
        data["sortable_name"] = agency["sortable_name"]
        data["slug"] = agency["slug"]
        list_of_agencies.append(data)
    return list_of_agencies

def get_title_and_chapter_from_agency(
        json_response,
        name=None,
        sortable_name=None,
        slug=None
    ):
    if name == None and \
        sortable_name == None and \
        slug == None:
        raise ValueError(
            "At least one of name, short_name, sortable_name, or slug must be provided")

    title_and_chapter = {}

    def get_cfr_references_from_any_children(agency):
        children = []
        if len(agency["children"]) > 0:
            for child in agency["children"]:
                child_data = {}

                if "name" in child:
                    child_data["name"] = child["name"]
                if "sortable_name" in child:
                    child_data["sortable_name"] = child["sortable_name"]
                if "slug" in child:
                    child_data["slug"] = child["slug"]
                if "cfr_references" in child:
                    child_data["cfr_references"] = child["cfr_references"]
                children.append(child_data)
        return children

    # O(N) (should be O(153)
    for agency in json_response["agencies"]:
        if name == agency["name"]:
            title_and_chapter = agency["cfr_references"]
            if len(agency["children"]) > 0:
                children = get_cfr_references_from_any_children(agency)
                title_and_chapter["children"] = children

            return title_and_chapter
        elif sortable_name == agency["sortable_name"]:
            title_and_chapter = agency["cfr_references"]
            if len(agency["children"]) > 0:
                children = get_cfr_references_from_any_children(agency)
                title_and_chapter["children"] = children
            return title_and_chapter
        elif slug == agency["slug"]:
            title_and_chapter = agency["cfr_references"]
            if len(agency["children"]) > 0:
                children = get_cfr_references_from_any_children(agency)
                title_and_chapter["children"] = children
            return title_and_chapter
    return None
