# Import necessary libraries and functions
import streamlit as st
import re
from logics.data_collector import LibraryMembershipDataCollector
from logics.library_search import generate_search_url, handle_query_intent
from logics.library_locations import load_library_locations
from helper_functions.llm import get_completion
from helper_functions.utility import check_password
from logics.library_locations import prepare_library_context


# Configure Streamlit page layout and title
st.set_page_config(layout="centered", page_title="LibConnect - Discover . Search . Connect")
st.title("📚 LibConnect")

# **Authentication Check**: Verify access using password utility; halt if authentication fails
if not check_password():
    st.stop()

# **Load Membership Data**: Instantiate LibraryMembershipDataCollector to manage membership info
text_path = 'data/membership.txt'
collector = LibraryMembershipDataCollector(text_path)

# **Load Library Locations**: Import library location data from JSON file
libraries = load_library_locations('data/libraries.json')

# **Prepare Library Context**: Format library location data for query processing
library_context = prepare_library_context(libraries)

# **Initialize Conversation History**: Establish session state to store conversation flow
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# **Input Sanitization**: Prevent prompt injection attacks by filtering certain commands
def sanitize_input(user_input):
    blacklist = ["ignore all", "shutdown", "delete", "execute", "run", "ignore previous instructions"]
    for word in blacklist:
        if word in user_input.lower():
            return "Input rejected due to suspicious content."
    return user_input

# **Keyword Extraction Function**: Remove common phrases and terms for clean keyword extraction
def extract_keywords(query):
    # List of phrases and words to ignore
    ignore_phrases = [
            "do you have", "can i find", "looking for", "look for", "i am", 
            "could you", "would you", "please", "show me", "tell me", 
            "give me", "i need", "i want", "is there", "can you", "help me with", "can i get", "you would"
        ]
    ignore_words = {
            "book", "books", "find", "show", "search", "for", "about", "of", "my", "the", 
            "recommend", "need", "want", "available", "some", "any", "all", "me", "that"
        }

    # Remove multi-word phrases from the query
    for phrase in ignore_phrases:
        query = query.lower().replace(phrase, "")

    # Split the remaining query into words and filter out ignored words
    words = re.findall(r'\w+', query.lower())  # Extract words and convert to lowercase
    keywords = [word for word in words if word not in ignore_words]
    
    return " ".join(keywords)

# **Prompt Chaining Logic**: Handle different types of user queries (membership, search, location)
def handle_prompt_chain(user_query):
    
    # **Identify Query Type**: Determine if the query is about membership, search, or location
    is_membership_query, is_search_query, is_location_query = handle_query_intent(user_query)

    # **Contextualize with Conversation History**: Use previous messages as context
    context = "\n".join(st.session_state.conversation)  # Get conversation history as context

    # **Membership Queries**: Generate response based on membership data
    if is_membership_query:
        prompt = (
            "You are a helpful virtual librarian assistant. Here's detailed information about library memberships:\n"
            f"{collector.membership_data}\n\n"
            f"Previous Conversation Context: {context}\n"  # Include previous context
            "Please answer the following membership query from the user:\n"
            f"{user_query}\n"
        )
        return get_completion(prompt)

    # **Book Search Queries**: Generate search results and relevant book suggestions
    if is_search_query:
        # Extract keywords from the user query
        refined_query = extract_keywords(user_query)
        search_url = generate_search_url(refined_query)  # Use refined query for search URL
        
        # Prompt with detailed guidance on book search and suggestions
        prompt = (
            "You are a helpful virtual librarian assistant. Here’s how to search for books in the library:\n"
            f"Previous Conversation Context: {context}\n"  # Include previous context
            "1. A direct link to search for books on the topic.\n"
            "2. A brief list of 2-3 popular or recommended books on the topic with brief description, if known. Include individual direct links to search these books using keywords from the user query.\n"
            #"3. Any digital resources or e-books related to the topic.\n\n"
            f"User Query: {user_query}\n"
            f"Extracted Keywords for Search: {refined_query}\n"
            f"Search Link: {search_url}\n"
            
    )
        print(refined_query)
        return get_completion(prompt)
    
    
    # **Location Queries**: Respond based on user’s location and previous context
    if is_location_query:
        # Check if a location context was provided earlier
        previous_location = None
        for message in reversed(st.session_state.conversation):
            if "at" in message.lower():
                previous_location = message.split()[-1]  # Extract the postal code, assuming it's the last word
                break

        # Construct response, considering previous location if available
        if previous_location:
            prompt = (
                "You are a helpful virtual librarian assistant. Here's detailed information about library locations, including their specific opening hours:\n"
                f"{library_context}\n\n"
                f"I see you mentioned being at postal code {previous_location} earlier. Based on this, let me find the nearest library for you, including their opening hours.\n"
                f"Current User Query: {user_query}\n"
            )
        else:
            prompt = (
                "You are a helpful virtual librarian assistant. Here's detailed information about library locations, including their specific opening hours:\n"
                f"{library_context}\n\n"
                f"Previous Conversation Context: {context}\n"
                f"Current User Query: {user_query}\n"
            )

        return get_completion(prompt)



    # **Fallback Response**: General response if query type is not identified
    return get_completion(f"Here’s the previous conversation context:\n{context}\n\nPlease answer the following query from a user:\n{user_query}\n")


# **Streamlit Form**: Create user input form for query submission
form = st.form(key="form")
form.subheader("Discover . Search . Connect")

user_query = form.text_area("How can I assist you today? Search for books, find library locations, or learn about memberships.", height=50)

if form.form_submit_button("**Submit**"):
    #st.toast(f"User Query Submitted - {user_query}")
    st.divider()

    try:
        # **Sanitize User Query**: Filter suspicious content
        sanitized_query = sanitize_input(user_query)
        if "Input rejected" in sanitized_query:
            st.write(sanitized_query)
        else:
            # **Handle Prompt Chaining**: Generate a response based on user query
            response = handle_prompt_chain(sanitized_query)
            
            # Display the response and update session conversation history
            st.write(response)

            # Add user query and assistant response to session state
            st.session_state.conversation.append(f"User: {sanitized_query}")
            st.session_state.conversation.append(f"Assistant: {response}")

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")

    st.divider()

# **Custom Chat Styling**: Enhance chat display with CSS for user and assistant bubbles
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

# **Clickable Links in Assistant Messages**: Detect URLs and format as clickable Markdown links
def make_links_clickable(text):
    url_pattern = r'https?://\S+'
    return re.sub(url_pattern, r'[Link](\g<0>)', text)  

# **Display Conversation History**: Format and display past interactions
st.write("**User Interaction History:**")
chat_container = st.container()  # Create a container for the chat

# Loop through the conversation in pairs and reverse the order
for idx in range(len(st.session_state.conversation) - 1, 0, -2):  # Step backward in pairs
    if idx < len(st.session_state.conversation):
        user_message = st.session_state.conversation[idx - 1].replace("User:", "").strip()
        assistant_message = st.session_state.conversation[idx].replace("Assistant:", "").strip()

        # Display user and assistant messages with custom bubble formatting
        st.markdown(f"<div class='user-bubble'>User: {user_message}</div>", unsafe_allow_html=True)        
        st.markdown(f"<div class='assistant-bubble'>Assistant: {assistant_message}</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)  # Optional horizontal line separator

# **Disclaimer**: Note about app’s limitations and usage intent
with st.expander("**❗️Disclaimer**", expanded=False):
    st.write("""                      
    This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.
    Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.    
    Always consult with qualified professionals for accurate and personalized advice.
    """)