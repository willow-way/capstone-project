import json


def load_library_locations(file_path):
    """Load library locations from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def prepare_library_context(libraries):
    context = "Here's a list of our libraries:\n\n"
    for library in libraries:
        context += f"- {library['name']}: {library['address']}\n"
    return context

def search_library_locations(user_query, libraries):
    """Return libraries that match the user query."""
    query_terms = user_query.lower().split()
    location_terms = [term for term in query_terms if term not in ["library", "at", "in", "near", "do", "you", "have"]]

    print(f"Searching for location terms: {location_terms}")  # Debug print

    best_match = None
    best_score = 0

    for library in libraries:
        library_name_lower = library['name'].lower()
        score = sum(term in library_name_lower for term in location_terms)
        if score > best_score:
            best_score = score
            best_match = library

    if best_match and best_score > 0:
        print(f"Found matching library: {best_match['name']}")  # Debug print
        return [best_match]

    print("No matching library found")  # Debug print
    return []  # Return an empty list if no match is found