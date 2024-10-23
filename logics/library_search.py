import urllib.parse
import re

BASE_LIBRARY_URL = "https://search.nlb.gov.sg/onesearch/Search"

def handle_query_intent(user_query):
    membership_terms = ["membership", "register", "join", "borrow", "renew", "loan", "rur", "repository", "enewspaper", "emagazine", "digital resource"]
    search_terms = ["book", "find", "search", "look for"]
    location_terms = ["library", "at", "in", "near"]

    is_membership_query = any(term in user_query.lower() for term in membership_terms)
    is_search_query = any(term in user_query.lower() for term in search_terms)
    is_location_query = any(term in user_query.lower() for term in location_terms)

    return is_membership_query, is_search_query, is_location_query

def extract_search_terms(user_input):
    """Extract the main search keyword from user input focusing on book-related topics."""
    # Strip unwanted phrases and focus on sections linked by 'books about', 'on', or 'for'
    match = re.search(r'\b(?:books? (?:about|on|for)?|about|on|for)\s+([^\.,!?]+)', user_input, re.IGNORECASE)

    if match:
        # Return the matched keyword that relates to the book search
        return match.group(1).strip()
    
    # Default case covers unmatched input
    return user_input.strip()

def generate_search_url(query, content_type="book"):
    search_term = extract_search_terms(query)
    if not search_term:
        raise ValueError("A valid search term must be provided.")

    search_params = {
        "query": search_term,
        "cont": content_type
    }

    url_encoded_params = urllib.parse.urlencode(search_params)
    return f"{BASE_LIBRARY_URL}?{url_encoded_params}"