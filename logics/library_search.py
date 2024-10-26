# Import necessary libraries
import urllib.parse
import re

# **Library Search Function**: Generate search URL for a given query
BASE_LIBRARY_URL = "https://search.nlb.gov.sg/onesearch/Search"

# **Handle Query Intent Function**: Identify the type of query and generate appropriate response
def handle_query_intent(user_query):
        # Define the conditions for different types of queries
    membership_terms = ["membership", "register", "join", "borrow", "renew", "loan", "rur", "repository", "enewspaper", "emagazine", "digital resource"]
    search_terms = ["book", "find", "search", "look for", "looking for", "catalogue", "catalog", "books", "book search", "book searches"]
    location_terms = ["library", "at", "in", "near", "libraries", "nearby", "location", "locations", "map", "location link", 
                      "Google Maps link", "directions", "direction", "Google Maps", "Maps", "map link", "navigate", 
                      "find directions", "route", "address link", "find on map", "how to get to", "open", "opening hours",
                      "close", "closing hours", "hours", "hours of operation", "operating hours", "operating hours of",
                      "what time", "what times", "when", "when is", "when is it", "when does", "when does it", "open time"]
                      

    is_membership_query = any(term in user_query.lower() for term in membership_terms)
    is_search_query = any(term in user_query.lower() for term in search_terms)
    is_location_query = any(term in user_query.lower() for term in location_terms)

    return is_membership_query, is_search_query, is_location_query

# **Extract Search Terms Function**: Extract the main search keyword from user input
def extract_search_terms(user_input):
    """Extract the main search keyword from user input focusing on book-related topics."""
    # Improved regex to capture phrases that involve authors or book titles
    match = re.search(r'\b(?:books? about|by|on|for|search for|find)\s+([^\.,!?]+)', user_input, re.IGNORECASE)

    if match:
        # Return the matched keyword that relates to the book search
        return match.group(1).strip()
    
    # Default case covers unmatched input
    return user_input.strip()

# **Generate Search URL Function**: Generate the search URL for a given query
def generate_search_url(query):
        # Use extract_search_terms to focus on the relevant parts
    search_term = extract_search_terms(query)
    if not search_term:
        raise ValueError("A valid search term must be provided.")

    search_params = {
        "query": search_term,  # This should only be the relevant term
        "cont": "book"
    }

    url_encoded_params = urllib.parse.urlencode(search_params)
    return f"{BASE_LIBRARY_URL}?{url_encoded_params}"