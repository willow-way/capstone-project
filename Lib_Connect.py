import streamlit as st
from logics.data_collector import LibraryMembershipDataCollector
from logics.library_search import generate_search_url, handle_query_intent
from logics.library_locations import load_library_locations
from helper_functions.llm import get_completion
from helper_functions.utility import check_password
from logics.library_locations import prepare_library_context

# Configure Streamlit
st.set_page_config(layout="centered", page_title="LibConnect - Discover . Search . Connect")

st.title("📚 LibConnect")

# Ensure password authentication using utility function
if not check_password():
    st.stop()

# Load membership data
text_path = 'data/membership.txt'
collector = LibraryMembershipDataCollector(text_path)

# Load library locations
libraries = load_library_locations('data/libraries.json')

# Prepare library context
library_context = prepare_library_context(libraries)

# Initialize session states for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Input sanitization to prevent prompt injection
def sanitize_input(user_input):
    blacklist = ["ignore all", "shutdown", "delete", "execute", "run", "ignore previous instructions"]
    for word in blacklist:
        if word in user_input.lower():
            return "Input rejected due to suspicious content."
    return user_input

# Prompt chaining logic
def handle_prompt_chain(user_query):
    # Determine the type of user query (membership, search, location)
    is_membership_query, is_search_query, is_location_query = handle_query_intent(user_query)
    
    context = "\n".join(st.session_state.conversation)  # Get conversation history as context

    # Step 1: Handle Membership-related Queries
    if is_membership_query:
        prompt = (
            "You are a helpful virtual librarian assistant. Here's detailed information about library memberships:\n"
            f"{collector.membership_data}\n\n"
            "Please answer the following membership query from the user:\n"
            f"{user_query}\n"
        )
        return get_completion(prompt)

    # Step 2: Handle Book Search Queries
    if is_search_query:
        search_url = generate_search_url(user_query)
        prompt = (
            "You are a helpful virtual librarian assistant. Here's how to search for books in the library:\n"
            "1. A direct link to search for books on the topic.\n"
            "2. A brief list of 2-3 popular or recommended books on the topic, if known. Include individual direct link to search these books.\n"
            "3. Any digital resources or e-books related to the topic.\n\n"
            f"User query: {user_query}\n\n"
            f"Here’s the search link: {search_url}\n"
        )
        return get_completion(prompt)

    # Step 3: Handle Location-related Queries
    if is_location_query:
        prompt = (
            "You are a helpful virtual librarian assistant. Here's information about library locations:\n"
            f"{library_context}\n\n"
            "If the user is asking for directions, provide the nearest library information and a Google Maps link to that library.\n"
            f"User query: {user_query}\n"
        )
        return get_completion(prompt)

    # If no specific type matches, return a fallback response
    return get_completion(f"Here’s the previous conversation context:\n{context}\n\nPlease answer the following query from a user:\n{user_query}\n")

# Start the Streamlit form
form = st.form(key="form")
form.subheader("Discover . Search . Connect")

user_query = form.text_area("How can I assist you today? Search for books, find library locations, or learn about memberships.", height=50)

if form.form_submit_button("**Submit**"):
    st.toast(f"User Query Submitted - {user_query}")
    st.divider()

    try:
        # Sanitize user input
        sanitized_query = sanitize_input(user_query)
        if "Input rejected" in sanitized_query:
            st.write(sanitized_query)
        else:
            # Handle prompt chaining and generate response
            response = handle_prompt_chain(sanitized_query)
            
            # Display the response
            st.write(response)

            # Add user query and assistant response to session state
            st.session_state.conversation.append(f"User: {sanitized_query}")
            st.session_state.conversation.append(f"Assistant: {response}")

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

    st.divider()

    # Display conversation history
    st.write("**Conversation History:**")
    for idx, message in enumerate(st.session_state.conversation, 1):
        st.write(f"{idx}. {message}")

# Add important notice below the text area
with st.expander("**❗️Disclaimer**", expanded=False):
    st.write("""
             
         
    This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.
    
    Always consult with qualified professionals for accurate and personalized advice.
    """)
