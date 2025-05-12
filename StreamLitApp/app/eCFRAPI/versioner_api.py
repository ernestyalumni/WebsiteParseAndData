import requests

BASE_URL = "https://www.ecfr.gov/api/versioner/v1"

def get_ancestry(
    date,
    title,
    subtitle=None,
    chapter=None,
    subchapter=None,
    part=None,
    subpart=None,
    section=None,
    appendix=None
):
    """
    Get all ancestors (including self) from a given level through the top title node.
    
    The Ancestry service can be used to determine the complete ancestry to a leaf node 
    at a specific point in time.
    
    Args:
        date (str): Date in YYYY-MM-DD format
        title (str): Title Number: '1', '2', '50', etc
        subtitle (str, optional): Uppercase letter. 'A', 'B', 'C'
        chapter (str, optional): Roman Numerals and digits 0-9. 'I', 'X', '1'
        subchapter (str, optional): Uppercase letters with optional underscore or dash. 'A', 'B', 'I'
                                   A SUBCHAPTER REQUIRES A CHAPTER.
        part (str, optional): Uppercase letters with optional underscore or dash. 'A', 'B', 'I'
        subpart (str, optional): Generally an uppercase letter. 'A', 'B', 'C'
                                A SUBPART REQUIRES A PART.
        section (str, optional): Generally a number followed by a dot and another number. '121.1', '13.4', '1.9'
                                A SECTION REQUIRES A PART.
        appendix (str, optional): Multiple formats. 'A', 'III', 'App. A'
                                 AN APPENDIX REQUIRES A SUBTITLE, CHAPTER or PART.
    
    Returns:
        tuple: (status_code, is_expected_status_code, response_data)
    
    Raises:
        RuntimeError: If a required parameter is missing based on hierarchy requirements
    """
    # Validate hierarchy requirements
    if subchapter and not chapter:
        raise RuntimeError("A SUBCHAPTER REQUIRES A CHAPTER")
    if subpart and not part:
        raise RuntimeError("A SUBPART REQUIRES A PART")
    if section and not part:
        raise RuntimeError("A SECTION REQUIRES A PART")
    if appendix and not (subtitle or chapter or part):
        raise RuntimeError("AN APPENDIX REQUIRES A SUBTITLE, CHAPTER or PART")
    
    url = f"{BASE_URL}/ancestry/{date}/title-{title}.json"
    headers = {"accept": "application/json"}
    
    # Build parameters dictionary
    params = {}
    
    # Add optional parameters if provided
    if subtitle:
        params["subtitle"] = subtitle
    if chapter:
        params["chapter"] = chapter
    if subchapter:
        params["subchapter"] = subchapter
    if part:
        params["part"] = part
    if subpart:
        params["subpart"] = subpart
    if section:
        params["section"] = section
    if appendix:
        params["appendix"] = appendix
    
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.status_code, response.status_code == 200, response.json() \
            if response.status_code == 200 else None
    except Exception as e:
        return 500, False, {"error": str(e)}

def get_title_source_route(
    date,
    title,
    subtitle=None,
    chapter=None,
    subchapter=None,
    part=None,
    subpart=None,
    section=None,
    appendix=None
):
    """
    Get source XML for a title or subset of a title.
    
    The title source route can be used to retrieve the source xml for a complete title or subset.
    The subset of xml is determined by the lowest leaf node given. For example, if you request 
    Title 1, Chapter I, Part 1, you'll receive the XML only for Part 1 and its children.
    
    Args:
        date (str): Date in YYYY-MM-DD format
        title (str): Title Number: '1', '2', '50', etc
        subtitle (str, optional): Uppercase letter. 'A', 'B', 'C'
        chapter (str, optional): Roman Numerals and digits 0-9. 'I', 'X', '1'
        subchapter (str, optional): Uppercase letters with optional underscore or dash. 'A', 'B', 'I'
                                   A SUBCHAPTER REQUIRES A CHAPTER.
        part (str, optional): Uppercase letters with optional underscore or dash. 'A', 'B', 'I'
        subpart (str, optional): Generally an uppercase letter. 'A', 'B', 'C'
                                A SUBPART REQUIRES A PART.
        section (str, optional): Generally a number followed by a dot and another number. '121.1', '13.4', '1.9'
                                A SECTION REQUIRES A PART.
        appendix (str, optional): Multiple formats. 'A', 'III', 'App. A'
                                 AN APPENDIX REQUIRES A SUBTITLE, CHAPTER or PART.
    
    Returns:
        tuple: (status_code, is_expected_status_code, response_data)
    
    Raises:
        RuntimeError: If a required parameter is missing based on hierarchy requirements
    """
    # Validate hierarchy requirements
    if subchapter and not chapter:
        raise RuntimeError("A SUBCHAPTER REQUIRES A CHAPTER")
    if subpart and not part:
        raise RuntimeError("A SUBPART REQUIRES A PART")
    if section and not part:
        raise RuntimeError("A SECTION REQUIRES A PART")
    if appendix and not (subtitle or chapter or part):
        raise RuntimeError("AN APPENDIX REQUIRES A SUBTITLE, CHAPTER or PART")
    
    url = f"{BASE_URL}/full/{date}/title-{title}.xml"
    headers = {"accept": "application/xml"}
    
    # Build parameters dictionary
    params = {}
    
    # Add optional parameters if provided
    if subtitle:
        params["subtitle"] = subtitle
    if chapter:
        params["chapter"] = chapter
    if subchapter:
        params["subchapter"] = subchapter
    if part:
        params["part"] = part
    if subpart:
        params["subpart"] = subpart
    if section:
        params["section"] = section
    if appendix:
        params["appendix"] = appendix
    
    try:
        response = requests.get(url, headers=headers, params=params)
        # For XML responses, return the text content instead of trying to parse
        # as JSON
        return response.status_code, response.status_code == 200, response.text \
            if response.status_code == 200 else None
    except Exception as e:
        return 500, False, {"error": str(e)}

def get_structure(date, title):
    """
    Get the complete structure of a title as JSON.
    
    The structure JSON endpoint returns the complete structure of a title back as json.
    This format does not include the content of the title but does include all structure
    and content nodes as well as their meta data including their type, label, description,
    identifier and children.
    
    Args:
        date (str): Date in YYYY-MM-DD format
        title (str): Title Number: '1', '2', '50', etc
    
    Returns:
        tuple: (status_code, is_expected_status_code, response_data)
    """
    url = f"{BASE_URL}/structure/{date}/title-{title}.json"
    headers = {"accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        return response.status_code, response.status_code == 200, response.json() \
            if response.status_code == 200 else None
    except Exception as e:
        return 500, False, {"error": str(e)}

def get_titles():
    """
    Get summary information about each title.
    
    The Title service can be used to determine the status of each individual title 
    and of the overall status of title imports and reprocessings. It returns an array 
    of all titles containing information for each with the name of the title, the latest 
    amended date, latest issue date, up-to-date date, reserved status, and if applicable, 
    processing in progress status.
    
    Returns:
        tuple: (status_code, is_expected_status_code, response_data)
    """
    url = f"{BASE_URL}/titles.json"
    headers = {"accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        return response.status_code, response.status_code == 200, response.json() \
            if response.status_code == 200 else None
    except Exception as e:
        return 500, False, {"error": str(e)}

def get_versions(
    title,
    issue_date_on=None,
    issue_date_lte=None,
    issue_date_gte=None,
    subtitle=None,
    chapter=None,
    subchapter=None,
    part=None,
    subpart=None,
    section=None,
    appendix=None
):
    """
    Get an array of all sections and appendices inside a title.
    
    Returns the content versions meeting the specified criteria. Each content object includes 
    its identifier, parent hierarchy, last amendment date and issue date it was last updated.
    
    Args:
        title (str): Title Number: '1', '2', '50', etc
        issue_date_on (str, optional): Select content added on the supplied issue date
        issue_date_lte (str, optional): Select content added on or before the supplied issue date
        issue_date_gte (str, optional): Select content added on or after the supplied issue date
        subtitle (str, optional): Uppercase letter. 'A', 'B', 'C'
        chapter (str, optional): Roman Numerals and digits 0-9. 'I', 'X', '1'
        subchapter (str, optional): Uppercase letters with optional underscore or dash. 'A', 'B', 'I'
                                   A SUBCHAPTER REQUIRES A CHAPTER.
        part (str, optional): Uppercase letters with optional underscore or dash. 'A', 'B', 'I'
        subpart (str, optional): Generally an uppercase letter. 'A', 'B', 'C'
                                A SUBPART REQUIRES A PART.
        section (str, optional): Generally a number followed by a dot and another number. '121.1', '13.4', '1.9'
                                A SECTION REQUIRES A PART.
        appendix (str, optional): Multiple formats. 'A', 'III', 'App. A'
                                 AN APPENDIX REQUIRES A SUBTITLE, CHAPTER or PART.
    
    Returns:
        tuple: (status_code, is_expected_status_code, response_data)
    
    Raises:
        RuntimeError: If a required parameter is missing based on hierarchy requirements
        RuntimeError: If issue_date_on is used with issue_date_lte or issue_date_gte
    """
    # Validate hierarchy requirements
    if subchapter and not chapter:
        raise RuntimeError("A SUBCHAPTER REQUIRES A CHAPTER")
    if subpart and not part:
        raise RuntimeError("A SUBPART REQUIRES A PART")
    if section and not part:
        raise RuntimeError("A SECTION REQUIRES A PART")
    if appendix and not (subtitle or chapter or part):
        raise RuntimeError("AN APPENDIX REQUIRES A SUBTITLE, CHAPTER or PART")
    
    # Validate issue_date parameters
    if issue_date_on and (issue_date_lte or issue_date_gte):
        raise RuntimeError("Use of the 'on' parameter precludes use of 'gte' or 'lte'")
    
    url = f"{BASE_URL}/versions/title-{title}.json"
    headers = {"accept": "application/json"}
    
    # Build parameters dictionary
    params = {}
    
    # Add issue_date parameters if provided
    if issue_date_on:
        params["issue_date[on]"] = issue_date_on
    if issue_date_lte:
        params["issue_date[lte]"] = issue_date_lte
    if issue_date_gte:
        params["issue_date[gte]"] = issue_date_gte
    
    # Add optional hierarchy parameters if provided
    if subtitle:
        params["subtitle"] = subtitle
    if chapter:
        params["chapter"] = chapter
    if subchapter:
        params["subchapter"] = subchapter
    if part:
        params["part"] = part
    if subpart:
        params["subpart"] = subpart
    if section:
        params["section"] = section
    if appendix:
        params["appendix"] = appendix
    
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.status_code, response.status_code == 200, response.json() \
            if response.status_code == 200 else None
    except Exception as e:
        return 500, False, {"error": str(e)}

