# Import necessary libraries
import json

# **Load Library Locations Function**: Read library locations from a JSON file
def load_library_locations(file_path):
    """Load library locations from a JSON file."""
    
    # Open the specified JSON file and parse it into Python objects
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# **Prepare Library Context Function**: Format library locations for display
def prepare_library_context(libraries):
    context = "Here's a list of our libraries with their addresses and operating hours:\n\n"
    for library in libraries:
        context += f"- {library['name']}\n  Address: {library['address']}\n  Opening Hours: {library['opening_hours']['general']}\n"
        
        # Include exceptions if available
        if 'exceptions' in library['opening_hours']:
            context += "  Exceptions: " + "; ".join(library['opening_hours']['exceptions']) + "\n"
        context += "\n"  # Add spacing for readability
    
    return context


# **Search Library Locations Function**: Find libraries that match the user query
def search_library_locations(user_query, libraries):
    """Return libraries that match the user query."""
    query_terms = user_query.lower().split()

    # Filter out common words that don't contribute to location matching
    location_terms = [term for term in query_terms if term not in ["library", "at", "in", "near", "do", "you", "have"]]

    print(f"Searching for location terms: {location_terms}")  # Debug print

    # Initialize variables to keep track of the best matching library and its score
    best_match = None
    best_score = 0

    # Iterate over each library to calculate a match score based on location terms
    for library in libraries:
        library_name_lower = library['name'].lower()
        score = sum(term in library_name_lower for term in location_terms)
        if score > best_score:
            best_score = score
            best_match = library

    # If a suitable match is found, return it; otherwise, indicate no match found
    if best_match and best_score > 0:
        print(f"Found matching library: {best_match['name']}")  # Debug print
        return [best_match]

    print("No matching library found")  # Debug print
    return []  # Return an empty list if no match is found