import streamlit as st
import re
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

def extract_keywords(query):
    # List of words to ignore (generic terms related to book searching)
    ignore_words = {"book", "books", "find", "show", "search", "for", "about", "of", "my", "the"}
    
    # Split query into words and filter out ignored words
    words = re.findall(r'\w+', query.lower())  # Extract words and convert to lowercase
    keywords = [word for word in words if word not in ignore_words]
    
    return " ".join(keywords)

# Prompt chaining logic
def handle_prompt_chain(user_query):
    # Determine the type of user query (membership, search, location)
    is_membership_query, is_search_query, is_location_query = handle_query_intent(user_query)

    # Prepare context from conversation history
    context = "\n".join(st.session_state.conversation)  # Get conversation history as context

    # Step 1: Handle Membership-related Queries
    if is_membership_query:
        prompt = (
            "You are a helpful virtual librarian assistant. Here's detailed information about library memberships:\n"
            f"{collector.membership_data}\n\n"
            f"Previous Conversation Context: {context}\n"  # Include previous context
            "Please answer the following membership query from the user:\n"
            f"{user_query}\n"
        )
        return get_completion(prompt)

    # Step 2: Handle Book Search Queries
    if is_search_query:
        # Extract keywords from the user query
        refined_query = extract_keywords(user_query)
        search_url = generate_search_url(refined_query)  # Use refined query for search URL
        
        # Now construct the prompt with refined keywords
        prompt = (
            "You are a helpful virtual librarian assistant. Here’s how to search for books in the library:\n"
            f"Previous Conversation Context: {context}\n"  # Include previous context
            "1. A direct link to search for books on the topic.\n"
            "2. A brief list of 2-3 popular or recommended books on the topic, if known. Include individual direct links to search these books using keywords from the user query.\n"
            "3. Any digital resources or e-books related to the topic.\n\n"
            f"User Query: {user_query}\n"
            f"Extracted Keywords for Search: {refined_query}\n"
            f"Search Link: {search_url}\n"
    )
        return get_completion(prompt)

    # Step 3: Handle Location-related Queries
    if is_location_query:
        # Check if a location context was provided earlier
        previous_location = None
        for message in reversed(st.session_state.conversation):
            if "at" in message.lower():
                previous_location = message.split()[-1]  # Extract the postal code, assuming it's the last word
                break

        # Provide a more informed answer based on previous location
        if previous_location:
            prompt = (
                "You are a helpful virtual librarian assistant. Here's information about library locations:\n"
                f"{library_context}\n\n"
                f"I see you mentioned being at postal code {previous_location} earlier. Let me find the nearest library for you.\n"
                f"Current User Query: {user_query}\n"
            )
        else:
            prompt = (
                "You are a helpful virtual librarian assistant. Here's information about library locations:\n"
                f"{library_context}\n\n"
                f"Previous Conversation Context: {context}\n"
                "If the user is asking for directions, provide the nearest library information and a Google Maps link to that library.\n"
                f"Current User Query: {user_query}\n"
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

# Add custom CSS for chat bubbles enhancing visual appearance for seamless chatting
st.markdown(
    """
    <style>
    .user-bubble {
        background-color: #d1f2d1; /* Light green for user */
        border-radius: 20px;
        padding: 10px;
        margin: 8px 10px 5px 10px; /* Add margin */
        max-width: 75%; /* Increased width for bubbles */
        align-self: flex-start;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* Shadow for depth */
        color: black; /* Black text color */
        display: inline-block; /* Ensure it behaves like a block element */
    }
    .assistant-bubble {
        background-color: #ffffff; /* White for assistant */
        border-radius: 20px;
        padding: 10px;
        margin: 8px 10px 5px 10px; /* Add margin */
        max-width: 75%; /* Increased width for assistant bubble */
        align-self: flex-end;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* Shadow for depth */
        border: 1px solid #e0e0e0; /* Subtle border */
        color: black; /* Black text color */
        display: inline-block; /* Ensure it behaves like a block element */
    }
    .chat-container {
        display: flex;
        flex-direction: column; /* Arrange messages from top to bottom */
        align-items: flex-start; /* Align user messages to the start */
        width: 100%; 
        padding: 20px; /* Padding for container */
        background-color: #f8f9fa; /* Light background for the chat area */
        border-radius: 10px; /* Rounded corners for the chat area */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to detect raw URLs and convert them to clickable Markdown links
def make_links_clickable(text):
    # This will match raw URLs and format them as Markdown clickable links
    url_pattern = r'https?://\S+'
    return re.sub(url_pattern, r'[Link](\g<0>)', text)  # Format correctly using \g<0> to reference the whole match

# Display Conversation History with Styling
st.write("**Conversation History:**")
chat_container = st.container()  # Create a container for the chat

# Loop through the conversation in pairs and reverse the order
for idx in range(len(st.session_state.conversation) - 1, 0, -2):  # Step backward in pairs
    if idx < len(st.session_state.conversation):
        user_message = st.session_state.conversation[idx - 1].replace("User:", "").strip()
        assistant_message = st.session_state.conversation[idx].replace("Assistant:", "").strip()

        # Display User message in a bubble
        st.markdown(f"<div class='user-bubble'>User: {user_message}</div>", unsafe_allow_html=True)

        # Display Assistant message in a bubble
        # Format the assistant message properly for clickable links
        st.markdown(f"<div class='assistant-bubble'>Assistant: {assistant_message}</div>", unsafe_allow_html=True)

        # Add a separator for better visual distinction
        st.markdown("<hr>", unsafe_allow_html=True)  # Optional horizontal line separator

# Add important notice below the text area
with st.expander("**❗️Disclaimer**", expanded=False):
    st.write("""
             
         
    This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.
    
    Always consult with qualified professionals for accurate and personalized advice.
    """)
